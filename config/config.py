# Bot Configuration
# Core settings and constants

import json
import os

# Admin/Developer phone number - has access to admin commands
# Format: phone number without @ or country code prefix
ADMIN_PHONE_NUMBER = "923453870090"

# Allowed chats - Only respond to messages from these chats/groups
# Maximum 3 chats allowed (Green API limit)
# Format for chats: phone number without @ (e.g., "923001234567")
# Format for groups: group ID without @ (e.g., "120363123456789012@g.us")
# Example: ["923001234567", "923009876543", "120363123456789012@g.us"]
ALLOWED_CHATS = [
    "923453870090"
    
    
]

# Database configuration (Turso)
TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL", "")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "")

# Link shortener API
ICE_BIO_API_KEY = os.getenv("ICE_BIO_API_KEY", "")


def get_prefix():
    # Returns the command prefix from commands.json
    try:
        commands_path = os.path.join('config', 'commands.json')
        with open(commands_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('prefix', '.')
    except Exception:
        return '.'


def is_admin(chat_id):
    # Check if a chat_id is from the admin user
    # chat_id format: "93779421543@c.us"
    # Returns True if the chat_id matches the admin phone number exactly
    
    clean_chat_id = chat_id.replace('@c.us', '').replace('@g.us', '').replace('+', '')
    return clean_chat_id == ADMIN_PHONE_NUMBER


def is_allowed_chat(chat_id):
    # Check if a chat_id is in the allowed chats list
    # chat_id format: "923001234567@c.us" or "120363123456789012@g.us"
    # Returns True if chat is allowed, or if ALLOWED_CHATS is empty (allow all)
    
    if not ALLOWED_CHATS:
        # Empty list means allow all chats
        return True
    
    # Check both with and without domain suffix
    clean_chat_id = chat_id.replace('@c.us', '').replace('@g.us', '')
    
    for allowed in ALLOWED_CHATS:
        # Remove @ suffix from allowed entry for comparison
        clean_allowed = allowed.replace('@c.us', '').replace('@g.us', '')
        if clean_chat_id == clean_allowed:
            return True
    
    return False
