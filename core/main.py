# Main Flask Application
# Single instance webhook support for Green API

import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from core.bot import handle_incoming_message
from core.api_requests import greenapi_set_credentials, greenapi_get_settings
from config.config import is_allowed_chat
from core.logger import log_initialization, log_bot_ready, log_webhook, log_ignored

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


def initialize_instance():
    """Initialize database and load Green API instance from environment"""
    global own_number, instance_id, token
    
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
        own_number = wid.replace('@c.us', '')
        
        if own_number:
            log_initialization(instance_id, own_number)
        else:
            print(f"⚠️ Instance initialized but couldn't get own number")
    else:
        print(f"⚠️ Instance initialized but couldn't fetch settings")
    
    log_bot_ready()


# Initialize instance on startup
initialize_instance()


@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhooks from Green API"""
    global own_number, instance_id, token
    
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        # Extract webhook type and log only if it's incoming message
        webhook_type = data.get('typeWebhook')
        log_webhook(webhook_type)
        
        # Ensure instance is set
        if instance_id and token:
            greenapi_set_credentials(instance_id, token)
        
        # Handle incoming messages only
        if webhook_type == 'incomingMessageReceived':
            message_data = data.get('messageData', {})
            sender_data = data.get('senderData', {})
            
            # Extract message details
            chat_id = sender_data.get('chatId')
            sender_name = sender_data.get('senderName', 'Unknown')
            
            # Check if message is from bot itself (ignore)
            if own_number and chat_id:
                sender_number = chat_id.replace('@c.us', '').replace('@g.us', '')
                if sender_number == own_number:
                    log_ignored('self')
                    return jsonify({"status": "ignored_self"}), 200
            
            # Check if chat is in allowed chats list
            if chat_id and not is_allowed_chat(chat_id):
                log_ignored('not_allowed', chat_id=chat_id)
                return jsonify({"status": "ignored_not_allowed"}), 200
            
            # Extract message text from different message types
            message_type = message_data.get('typeMessage')
            message_text = ''
            
            if message_type == 'textMessage':
                message_text = message_data.get('textMessageData', {}).get('textMessage', '')
            elif message_type == 'extendedTextMessage':
                message_text = message_data.get('extendedTextMessageData', {}).get('text', '')
            
            if chat_id and message_text:
                # Route to bot command handler
                handle_incoming_message(chat_id, message_text, sender_name)
            else:
                print(f"Missing chat_id or message_text")
        
        # Add line break separator between webhook requests
        print("ㅤ")
        
        return jsonify({"status": "received"}), 200
        
    except Exception as e:
        print(f"Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        
        # Add line break separator even on error
        print("ㅤ")
        
        # Still return 200 to prevent webhook retry loops
        return jsonify({"status": "error", "message": str(e)}), 200


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
