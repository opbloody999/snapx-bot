# ChatGPT Integration
# Provides conversational AI chat using BatGPT API
# Maintains chat sessions for conversation continuity

import time
from config.messages import get_message
from core.api_requests import chatgpt_send_message
from core.logger import log_gpt_operation, log_api_error

# ==================== SESSION MANAGEMENT ====================

# State management - tracks active chats and session IDs
active_chats = {}  # {chat_id: True/False}
chat_sessions = {}  # {chat_id: gpt_chat_id}
last_activity = {}  # {chat_id: timestamp}


def activate_chatbot(chat_id):
    # Enable ChatGPT mode for this chat
    active_chats[chat_id] = True
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = None
    last_activity[chat_id] = time.time()
    log_gpt_operation('activated', chat_id)
    
    # Return message key instead of hardcoded text
    return "gpt_activated"


def deactivate_chatbot(chat_id):
    # Disable ChatGPT mode for this chat
    active_chats[chat_id] = False
    log_gpt_operation('deactivated', chat_id)
    return get_message("gpt_deactivated_simple")


def is_chatbot_active(chat_id):
    # Check if ChatGPT mode is currently active
    return active_chats.get(chat_id, False)


def reset_chat_session(chat_id):
    # Clear chat history for this user
    chat_sessions[chat_id] = None


def get_last_activity(chat_id):
    # Get timestamp of last activity for this chat
    return last_activity.get(chat_id)


def update_last_activity(chat_id):
    # Update the last activity timestamp for this chat
    last_activity[chat_id] = time.time()


# ==================== TEXT FORMATTING ====================

def format_for_whatsapp(text):
    # Convert ChatGPT markdown to WhatsApp-compatible format
    # - Remove # symbols from headings (###, ##, #)
    # - Convert ** (bold) to * (WhatsApp bold)
    
    if not text:
        return text
    
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Remove leading hashes from headings (###, ##, #)
        stripped = line.lstrip()
        if stripped.startswith('#'):
            # Count and remove hashes
            hash_count = 0
            for char in stripped:
                if char == '#':
                    hash_count += 1
                else:
                    break
            # Remove hashes and any space after them
            line = stripped[hash_count:].lstrip()
        
        # Replace ** with * for WhatsApp bold formatting
        line = line.replace('**', '*')
        
        formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)


# ==================== API COMMUNICATION ====================


def send_to_chatgpt(message, chat_id):
    # Send message to ChatGPT and get response
    # Returns: (response_text, new_chat_id) or (None, None) on error
    
    gpt_chat_id = chat_sessions.get(chat_id)
    
    # Call API via centralized handler
    result = chatgpt_send_message(message, gpt_chat_id)
    
    if not result.get('success'):
        # Handle different error types
        error_type = result.get('error_type')
        
        if error_type == 'timeout':
            log_api_error('ChatGPT', 'timeout', 'Request timed out after 30 seconds')
            return get_message("gpt_timeout"), None
        elif error_type == 'http_error':
            log_api_error('ChatGPT', 'http_error', f"Status: {result.get('status_code')}")
            return None, None
        elif error_type == 'no_response':
            log_api_error('ChatGPT', 'no_response', f"Raw data: {result.get('raw_data')}")
            return get_message("gpt_no_response"), None
        elif error_type == 'connection_error':
            log_api_error('ChatGPT', 'connection_error', result.get('error'))
            return get_message("gpt_connection_error"), None
        else:
            log_api_error('ChatGPT', 'processing_error', result.get('error'))
            return get_message("gpt_processing_error"), None
    
    # Extract response and chat ID
    gpt_response = result.get('response')
    new_chat_id = result.get('chat_id')
    
    # Save chat ID for continuity
    if new_chat_id and new_chat_id != gpt_chat_id:
        chat_sessions[chat_id] = new_chat_id
    
    # Format response for WhatsApp compatibility
    formatted_response = format_for_whatsapp(gpt_response)
    
    return formatted_response, new_chat_id
