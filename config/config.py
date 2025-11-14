# Bot Configuration
# Core settings and constants

import json
import os

# Admin/Developer phone number - has access to admin commands
# Format: phone number without @ or country code prefix
# This will be automatically set to the instance owner's number on startup
ADMIN_PHONE_NUMBER = "923453870090"

# Note: Allowed chats are now informational only (displayed at startup)
# The bot will respond to ALL incoming webhooks with commands

# Database configuration (Turso)
TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL", "")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "")

# Link shortener API
ICE_BIO_API_KEY = os.getenv("ICE_BIO_API_KEY", "")

def load_settings():
    # Load settings from settings.json (no caching - always reads fresh)
    try:
        settings_path = os.path.join('config', 'settings.json')
        with open(settings_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"features": {}}


def show_raw_webhook_logs():
    # Check if raw webhook logging is enabled (reads fresh from file each time)
    settings = load_settings()
    return settings.get('features', {}).get('raw_webhook_logging', False)


def get_prefix():
    # Returns the command prefix from commands.json
    try:
        commands_path = os.path.join('config', 'commands.json')
        with open(commands_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('prefix', '.')
    except Exception:
        return '.'


def set_admin_number(phone_number):
    # Set the admin phone number dynamically
    global ADMIN_PHONE_NUMBER
    ADMIN_PHONE_NUMBER = phone_number


def is_admin(chat_id):
    # Check if a chat_id is from the admin user
    # chat_id format: "93779421543@c.us"
    # Returns True if the chat_id matches the admin phone number exactly
    
    clean_chat_id = chat_id.replace('@c.us', '').replace('@g.us', '').replace('+', '')
    return clean_chat_id == ADMIN_PHONE_NUMBER
