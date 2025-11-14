# Main Flask Application
# Single instance webhook support for Green API

import os
import logging
import re
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from core.bot import handle_incoming_message
from core.api_requests import greenapi_set_credentials, greenapi_get_settings, greenapi_get_group_data, greenapi_get_contact_info
from core.database import save_allowed_chats, get_allowed_chats
from core.logger import log_initialization, log_bot_ready, log_webhook, log_ignored, log_raw_request, log_raw_response, log_allowed_chats_display
from config.config import set_admin_number

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Disable Flask request logging (removes spam logs)
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

# Store own number to ignore self-messages
own_number = None
instance_id = None
token = None
instance_ready = False  # Flag to ensure initialization is complete


def normalize_user_id(user_id_raw):
    # Normalize user ID to consistent format for tracking and admin checks
    # Strips all WhatsApp suffixes (@c.us, @g.us, @s.whatsapp.net) and returns bare number
    # Returns: bare number string or None if invalid
    if not user_id_raw:
        return None
    
    # Strip common WhatsApp suffixes
    user_id = str(user_id_raw).replace('@c.us', '').replace('@g.us', '').replace('@s.whatsapp.net', '').replace('+', '')
    
    # Return normalized ID (bare number)
    return user_id if user_id else None


def initialize_instance():
    # Initialize database and load Green API instance from environment
    global own_number, instance_id, token, instance_ready
    
    # Load single instance credentials
    instance_id = os.getenv("GREEN_API_INSTANCE_ID")
    token = os.getenv("GREEN_API_TOKEN")
    
    if not instance_id or not token:
        print("ERROR: No Green API instance configured!")
        print("Please set GREEN_API_INSTANCE_ID and GREEN_API_TOKEN in Replit Secrets")
        exit(1)
    
    # Set current instance
    greenapi_set_credentials(instance_id, token)
    
    # Fetch own number from Green API
    settings = greenapi_get_settings()
    
    if settings:
        wid = settings.get('wid', '')
        own_number = wid.replace('@c.us', '').replace('@g.us', '').replace('+', '')
        
        if own_number:
            log_initialization(instance_id, own_number)
            instance_ready = True  # Mark instance as ready
        else:
            print(f"⚠️ Instance initialized but couldn't get own number")
    else:
        print(f"⚠️ Instance initialized but couldn't fetch settings")
    
    # Display allowed chats if any exist
    allowed_chats = get_allowed_chats()
    if allowed_chats:
        log_allowed_chats_display(allowed_chats)
    
    log_bot_ready()


# Initialize instance on startup
initialize_instance()


# Helper function to get chat name from Green API
def get_chat_name(chat_id):
    # Get name for a contact or group
    try:
        # Check if it's a group (ends with @g.us)
        if '@g.us' in chat_id:
            # It's a group - get group data
            group_data = greenapi_get_group_data(chat_id)
            if group_data and group_data.get('subject'):
                return group_data.get('subject')
            else:
                return chat_id
        else:
            # It's a contact - get contact info
            contact_data = greenapi_get_contact_info(chat_id)
            if contact_data and contact_data.get('name'):
                return contact_data.get('name')
            else:
                return chat_id
    except Exception:
        return chat_id


# Handle quota exceeded and save allowed chats
def handle_quota_exceeded(quota_data):
    try:
        # Extract chat IDs from description
        description = quota_data.get('description', '')
        
        # Extract chat IDs using regex (look for patterns like: 10001234560@c.us, 10001234561@c.us)
        chat_id_pattern = r'(\d+@[cg]\.us)'
        chat_ids = re.findall(chat_id_pattern, description)
        
        if not chat_ids:
            print("⚠️  Quota exceeded but no chat IDs found in description")
            return
        
        # Get names for each chat
        chats_data = []
        for chat_id in chat_ids:
            name = get_chat_name(chat_id)
            chats_data.append({
                'chat_id': chat_id,
                'name': name
            })
        
        # Save to database (only updates if chats changed)
        data_changed = save_allowed_chats(chats_data)
        
        # Only log if data actually changed (prevents console spam)
        if data_changed:
            print("\n" + "="*60)
            print("🚫 QUOTA EXCEEDED - Bot now restricted to 3 chats")
            print("="*60)
            print("\n✅ Allowed Chats:")
            for i, chat in enumerate(chats_data, 1):
                chat_type = "📱" if "@c.us" in chat['chat_id'] else "👥"
                print(f"  {i}. {chat_type} {chat['name']}")
                print(f"     ID: {chat['chat_id']}")
            print("\n" + "="*60)
            print("Bot will ignore all other chats/groups")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"Error handling quota exceeded: {e}")
        import traceback
        traceback.print_exc()


@app.route('/webhook', methods=['POST'])
def webhook():
    # Handle incoming webhooks from Green API
    global own_number, instance_id, token
    
    try:
        data = request.json
        
        if not data:
            response_data = {"error": "No data received"}
            log_raw_response('Webhook', response_data, 400)
            return jsonify(response_data), 400
        
        # Log raw incoming webhook
        log_raw_request('Webhook', data)
        
        # Extract webhook type and log only if it's incoming message
        webhook_type = data.get('typeWebhook')
        log_webhook(webhook_type)
        
        # Ensure instance is set
        if instance_id and token:
            greenapi_set_credentials(instance_id, token)
        
        # Handle quota exceeded webhook (still save allowed chats for display)
        if webhook_type == 'quotaExceeded':
            quota_data = data.get('quotaData', {})
            handle_quota_exceeded(quota_data)
            response_data = {"status": "quota_handled"}
            log_raw_response('Webhook', response_data, 200)
            return jsonify(response_data), 200
        
        # Handle incoming and outgoing messages
        if webhook_type == 'incomingMessageReceived' or webhook_type == 'outgoingMessageReceived':
            message_data = data.get('messageData', {})
            sender_data = data.get('senderData', {})
            
            # Extract message details based on webhook type
            if webhook_type == 'incomingMessageReceived':
                # Incoming: Use senderData for chat and sender info
                chat_id = sender_data.get('chatId')
                sender = sender_data.get('sender')
                sender_name = sender_data.get('senderName', 'Unknown')
                
                # Normalize user_id for consistent tracking and admin checks
                # Prefer sender (individual in group or direct chat), fallback to chatId
                user_id = normalize_user_id(sender if sender else chat_id)
                    
            else:  # outgoingMessageReceived
                # Outgoing: The bot owner sent this message
                # Skip if instance not ready to avoid race conditions
                if not instance_ready or not own_number:
                    print("⚠️ Skipping outgoing webhook - instance not ready")
                    response_data = {"status": "instance_not_ready"}
                    log_raw_response('Webhook', response_data, 200)
                    return jsonify(response_data), 200
                
                chat_id = sender_data.get('chatId') if sender_data else None
                
                # For outgoing, use sender if available, otherwise use own_number
                # Normalize to ensure consistent format
                sender_raw = sender_data.get('sender') if sender_data else own_number
                user_id = normalize_user_id(sender_raw)
                sender_name = 'You'
            
            # Extract message text from different message types
            message_type = message_data.get('typeMessage')
            message_text = ''
            
            if message_type == 'textMessage':
                message_text = message_data.get('textMessageData', {}).get('textMessage', '')
            elif message_type == 'extendedTextMessage':
                message_text = message_data.get('extendedTextMessageData', {}).get('text', '')
            elif message_type == 'quotedMessage':
                # For quoted messages (replies), text is in extendedTextMessageData
                message_text = message_data.get('extendedTextMessageData', {}).get('text', '')
            
            if chat_id and message_text and user_id:
                # Route to bot command handler with both chat_id (reply target) and user_id (tracking)
                handle_incoming_message(chat_id, user_id, message_text, sender_name)
            else:
                print(f"Missing required fields: chat_id={chat_id}, user_id={user_id}, message_text={'present' if message_text else 'missing'}")
        
        # Add line break separator between webhook requests
        print("ㅤ")
        
        response_data = {"status": "received"}
        log_raw_response('Webhook', response_data, 200)
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        
        # Add line break separator even on error
        print("ㅤ")
        
        response_data = {"status": "error", "message": str(e)}
        log_raw_response('Webhook', response_data, 200)
        
        # Still return 200 to prevent webhook retry loops
        return jsonify(response_data), 200


@app.route('/', methods=['GET'])
def home():
    # Health check endpoint
    return jsonify({
        "status": "running",
        "bot": "SnapX WhatsApp Bot",
        "instance": instance_id[:6] + "..." if instance_id else "Not configured",
        "endpoint": "/webhook"
    })


# Run the Flask app
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
