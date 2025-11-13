# Bot Command Router and Menu Builder
# Handles intelligent command parsing, routing, and menu generation

import json
import os
import time
import re
from difflib import get_close_matches

# Import config and messages
from config.config import get_prefix, is_admin
from config.messages import get_message

# Import logger
from core.logger import (
    log_incoming_message, log_command, log_command_blocked,
    log_greeting, log_gpt_activated, log_gpt_deactivated,
    log_ignored
)

# Import command handlers
from commands.chatbot import (
    activate_chatbot,
    deactivate_chatbot,
    is_chatbot_active,
    send_to_chatgpt,
    get_last_activity,
    update_last_activity
)
from commands.video_downloader import (
    download_video,
    get_supported_platforms,
    extract_url
)
from commands.whatsapp_tools import (
    handle_checkwhatsapp,
    handle_getavatar,
    handle_getcontactinfo
)
from commands.link_shortener import (
    handle_shortener_command,
    handle_mylinks_command,
    handle_stats_command
)
from commands.admin import (
    handle_alllinks_command,
    handle_videoonly_command
)

# Import Green API functions
from core.api_requests import greenapi_send_message as send_message, greenapi_send_file_by_url as send_file_by_url, greenapi_send_file_by_upload as send_file_by_upload

# Import database functions
from core.database import track_user, is_video_only_group, add_video_only_group, remove_video_only_group


# Load commands configuration
def load_commands():
    commands_path = os.path.join('config', 'commands.json')
    try:
        with open(commands_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Error loading commands: {e}")
        return {"commands": {}, "prefix": ".", "features": {}}


# Check if message is a URL
def is_url(text):
    url_pattern = r'https?://[^\s]+'
    return bool(re.search(url_pattern, text))


# Check if message is a greeting
def is_greeting(text):
    greetings = ['hi', 'hello', 'hey', 'greetings', 'hola', 'salaam', 'salam']
    text_lower = text.lower().strip()
    return text_lower in greetings or text_lower.startswith(tuple(greetings))


# Genius fuzzy match command - handles typos, missing dots, spacing mistakes
def fuzzy_match_command(text):
    config = load_commands()
    commands = config.get('commands', {})
    
    # Clean the text - remove dots, normalize to lowercase
    clean_text = text.strip().lower().replace('.', '')
    
    if not clean_text:
        return None
    
    # Build list of all valid command aliases with metadata
    all_aliases = []
    alias_to_data = {}
    
    for cmd_name, cmd_data in commands.items():
        aliases = cmd_data.get('aliases', [cmd_name])
        handler = cmd_data.get('handler')
        admin_only = cmd_data.get('admin_only', False)
        for alias in aliases:
            alias_lower = alias.lower()
            all_aliases.append(alias_lower)
            alias_to_data[alias_lower] = {
                'handler': handler,
                'admin_only': admin_only
            }
    
    # Try exact match first (with spaces preserved)
    if clean_text in alias_to_data:
        return alias_to_data[clean_text]
    
    # Try without spaces - handles "check whatsapp" -> "checkwhatsapp"
    no_spaces = clean_text.replace(' ', '')
    
    # Direct match without spaces
    if no_spaces in alias_to_data:
        return alias_to_data[no_spaces]
    
    # Strategy 1: Check if any alias matches with spaces removed
    for alias in all_aliases:
        alias_no_space = alias.replace(' ', '')
        if no_spaces == alias_no_space:
            return alias_to_data[alias]
    
    # Minimum length requirement for fuzzy matching (prevent ".a" matching "ai")
    # Require at least 2 characters for fuzzy matching to allow "gp" to match "gpt"
    if len(no_spaces) < 2:
        return None
    
    # Strategy 2: Levenshtein distance with strict length gating
    def levenshtein_distance(s1, s2):
        # Simple Levenshtein distance calculation
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    # Find best match with Levenshtein distance
    best_match = None
    best_distance = float('inf')
    
    for alias in all_aliases:
        # Remove spaces from both for comparison
        alias_clean = alias.replace(' ', '')
        
        # Strict length check BEFORE computing distance
        # Reject if length difference is too large (prevents matching "checkwhatsapp123" to "checkwhatsapp")
        length_diff = abs(len(no_spaces) - len(alias_clean))
        if length_diff > 3:  # Increased tolerance from 2 to 3
            continue
        
        distance = levenshtein_distance(no_spaces, alias_clean)
        
        # Allow more mistakes for better fuzzy matching
        max_distance = 1 if len(alias_clean) <= 4 else 2 if len(alias_clean) <= 8 else 3
        
        if distance <= max_distance and distance < best_distance:
            best_distance = distance
            best_match = alias
    
    if best_match:
        return alias_to_data[best_match]
    
    # Strategy 3: Use difflib as fallback with relaxed threshold
    # Only match if length difference is small (prevent matching "checkwhatsapp123" to "checkwhatsapp")
    aliases_no_space = [a.replace(' ', '') for a in all_aliases]
    matches = get_close_matches(no_spaces, aliases_no_space, n=1, cutoff=0.7)  # Lowered from 0.8 to 0.7
    if matches:
        matched_alias_clean = matches[0]
        # Check length difference - reject if too different
        length_diff = abs(len(no_spaces) - len(matched_alias_clean))
        if length_diff <= 3:  # Increased from 2 to 3
            # Find original alias
            for alias in all_aliases:
                if alias.replace(' ', '') == matched_alias_clean:
                    return alias_to_data[alias]
    
    return None


# Parse command and arguments
def parse_message(message_text):
    # Check if it's a greeting (only if short message)
    if len(message_text.split()) <= 3 and is_greeting(message_text):
        return {'handler': 'greeting', 'admin_only': False}, ''
    
    # Check if message starts with command prefix or command word
    prefix = get_prefix()
    is_command_syntax = message_text.strip().startswith(prefix)
    
    # Also check if message starts with any command word (for commands without prefix)
    first_word = message_text.strip().split()[0].lower() if message_text.strip() else ""
    
    # Load commands to check if first word matches any command
    commands_config = load_commands()
    all_command_names = []
    for cmd_key, cmd_data in commands_config.get('commands', {}).items():
        all_command_names.append(cmd_key.lower())
        all_command_names.extend([alias.lower() for alias in cmd_data.get('aliases', [])])
    
    starts_with_command = first_word in all_command_names
    
    # Check if it's a URL (auto video download) - must be primary content
    # BUT NOT if it starts with a command prefix OR command word
    if is_url(message_text) and not is_command_syntax and not starts_with_command:
        # Only treat as auto-download if URL is the primary message (not embedded in long text)
        words = message_text.split()
        url_count = sum(1 for word in words if 'http' in word)
        if url_count >= 1 and len(words) <= 5:  # URL with minimal surrounding text
            return {'handler': 'auto_download', 'admin_only': False}, message_text
    
    # Try to parse as command
    prefix = get_prefix()
    
    # Handle with or without prefix
    if message_text.startswith(prefix):
        command_part = message_text[len(prefix):].strip()
    else:
        command_part = message_text.strip()
    
    if not command_part:
        return None, None
    
    # CRITICAL FIX: Only match commands if message is SHORT (not a long chat message)
    # If message is too long, it's likely a normal conversation that happens to contain command words
    tokens = command_part.split()
    
    # Reject if message is too long (more than 15 words likely not a command)
    if len(tokens) > 15:
        return None, None
    
    # Strategy: Try to match progressively GROWING prefixes (shortest to longest)
    # This prevents args from being consumed by fuzzy matching
    # e.g., ".check whatsapp 123" tries "check", then "check whatsapp", matches at 2 words
    
    # Try matching first i tokens as command, from 1 to n
    # But limit to first 5 tokens to avoid matching in middle of long messages
    max_tokens_to_check = min(5, len(tokens))
    
    for i in range(1, max_tokens_to_check + 1):
        potential_cmd = ' '.join(tokens[:i])
        command_data = fuzzy_match_command(potential_cmd)
        
        if command_data:
            # Found command match - rest is args
            args = ' '.join(tokens[i:]) if i < len(tokens) else ""
            return command_data, args
    
    # No match found
    return None, None


# Handle greeting
def handle_greeting(chat_id, sender_name):
    name = f" {sender_name}" if sender_name else ""
    greeting_text = get_message("greeting", name=name)
    send_message(chat_id, greeting_text)
    log_greeting(sender_name)


# Handle menu command
def handle_menu_command(chat_id):
    menu_message = get_message("menu")
    send_message(chat_id, menu_message)


# Handle chatbot command
def handle_chatbot_command(chat_id, args):
    args = args.lower().strip()
    
    if args in ["on", "activate", "enable", "start", "yes"]:
        message_key = activate_chatbot(chat_id)
        send_message(chat_id, get_message(message_key))
        log_gpt_activated(chat_id)
    elif args in ["off", "deactivate", "disable", "stop", "no"]:
        deactivate_chatbot(chat_id)
        send_message(chat_id, get_message("gpt_deactivated"))
        log_gpt_deactivated(chat_id)
    else:
        send_message(chat_id, get_message("gpt_usage"))


# Handle auto video download
def handle_auto_download(chat_id, message_text, silent=False):
    """
    Handle video download
    silent: If True, don't send confirmation messages (for video-only mode)
    """
    url = extract_url(message_text)
    
    if not url:
        if not silent:
            send_message(chat_id, get_message("download_usage"))
        return
    
    if not silent:
        send_message(chat_id, get_message("downloading_video"))
    
    try:
        result = download_video(url)
        
        if not result or not result.get('success'):
            if not silent:
                send_message(chat_id, get_message("video_download_failed"))
            return
        
        video_url = result.get('media_url')
        title = result.get('title', 'Video')
        
        if not video_url:
            if not silent:
                send_message(chat_id, get_message("video_download_failed"))
            return
        
        # Send video using Green API
        caption = f"✅ {title}" if not silent else None
        filename = "video.mp4"
        
        response = send_file_by_url(chat_id, video_url, filename, caption)
        
        if response:
            # Video sent successfully - no log needed (already logged by logger)
            pass
        else:
            # Fallback: send download link (only if not silent)
            if not silent:
                send_message(
                    chat_id,
                    get_message("video_sent_fallback", video_url=video_url)
                )
            
    except Exception as e:
        print(f"Error in auto download: {e}")
        import traceback
        traceback.print_exc()
        if not silent:
            send_message(chat_id, get_message("video_download_failed"))


# Handle ChatGPT message
def handle_chatgpt_message(chat_id, message_text):
    # Update last activity
    update_last_activity(chat_id)
    
    # Send message to ChatGPT
    gpt_response, chat_id_gpt = send_to_chatgpt(message_text, chat_id)
    
    if gpt_response:
        send_message(chat_id, gpt_response)
    else:
        send_message(chat_id, get_message("chatgpt_error"))


# Handle dev menu command
def handle_dev_menu(chat_id):
    send_message(chat_id, get_message("dev_menu"))


# Handle admin commands (now public)
def handle_checkwhatsapp_command(chat_id, args):
    result = handle_checkwhatsapp(args)
    send_message(chat_id, result['message'])


def handle_getavatar_command(chat_id, args):
    result = handle_getavatar(args)
    send_message(chat_id, result['message'])
    
    # If avatar file was downloaded, send it
    if result.get('file_path'):
        try:
            import os
            response = send_file_by_upload(chat_id, result['file_path'], 'avatar.jpg')
            # Clean up temp file
            if os.path.exists(result['file_path']):
                os.remove(result['file_path'])
        except Exception as e:
            print(f"Error sending avatar file: {e}")


def handle_getcontactinfo_command(chat_id, args):
    response = handle_getcontactinfo(args)
    send_message(chat_id, response)


# Handle link shortener commands
def handle_link_shortener(chat_id, args):
    result = handle_shortener_command(chat_id, args)
    send_message(chat_id, result['message'])


def handle_my_links(chat_id):
    response = handle_mylinks_command(chat_id)
    send_message(chat_id, response)


def handle_stats(chat_id, args):
    response = handle_stats_command(chat_id, args)
    send_message(chat_id, response)


def handle_all_links_admin(chat_id):
    response = handle_alllinks_command()
    send_message(chat_id, response)


# Check and handle ChatGPT timeout
def check_chatgpt_timeout(chat_id):
    config = load_commands()
    timeout_minutes = config.get('features', {}).get('chatgpt_timeout_minutes', 5)
    
    if is_chatbot_active(chat_id):
        last_activity = get_last_activity(chat_id)
        if last_activity:
            inactive_time = time.time() - last_activity
            if inactive_time > (timeout_minutes * 60):
                deactivate_chatbot(chat_id)
                send_message(
                    chat_id, 
                    get_message("gpt_auto_timeout", minutes=timeout_minutes)
                )
                return True
    return False


# Main message handler
def handle_incoming_message(chat_id, message_text, sender_name):
    # Log incoming message
    log_incoming_message(sender_name, chat_id, message_text)
    
    # Track user interaction in database
    track_user(chat_id)
    
    # Check if this is a video-only group
    is_video_only = is_video_only_group(chat_id)
    is_dev = is_admin(chat_id)
    
    if is_video_only and not is_dev:
        # Video-only mode: Only process video downloads, silently
        if is_url(message_text):
            handle_auto_download(chat_id, message_text, silent=True)
        else:
            # Log that we're ignoring non-video message in video-only group
            log_ignored('video_only', group_id=chat_id)
        # Ignore all other messages (no response)
        return
    
    # Check for ChatGPT timeout
    check_chatgpt_timeout(chat_id)
    
    # Check if ChatGPT mode is active
    if is_chatbot_active(chat_id):
        # Special case: Check if message is trying to turn off GPT (with or without dot)
        msg_lower = message_text.strip().lower()
        
        # Check for GPT off patterns (gpt off, chatgpt off, .gpt off, etc.)
        gpt_off_patterns = ['gpt off', 'chatgpt off', 'gptoff', 'chatgptoff', 'ai off']
        is_gpt_off_command = any(pattern in msg_lower.replace(' ', '') or pattern in msg_lower for pattern in gpt_off_patterns)
        
        if is_gpt_off_command:
            # Deactivate GPT and send confirmation
            deactivate_chatbot(chat_id)
            send_message(chat_id, get_message("gpt_deactivated"))
            return
        
        # Check if this is an explicit command (starts with .)
        command_data, args = parse_message(message_text)
        
        # Only deactivate GPT if it's an explicit command with . prefix
        # Ignore greetings and other non-command patterns
        if command_data and message_text.strip().startswith('.'):
            # Explicit command detected - deactivate ChatGPT silently and run command
            deactivate_chatbot(chat_id)
        else:
            # Everything else (URLs, greetings, regular messages) goes to ChatGPT
            handle_chatgpt_message(chat_id, message_text)
            return
    
    # Parse message
    command_data, args = parse_message(message_text)
    
    if not command_data:
        # Not a recognized command or pattern - ignore (no logging needed)
        return
    
    handler = command_data.get('handler')
    admin_only = command_data.get('admin_only', False)
    
    # Log command detection
    log_command(handler, args or '', admin_only)
    
    # Check admin permissions for admin-only commands
    if admin_only and not is_admin(chat_id):
        send_message(chat_id, get_message("admin_only"))
        log_command_blocked(chat_id)
        return
    
    # Route to appropriate handler
    if handler == 'greeting':
        handle_greeting(chat_id, sender_name)
    elif handler == 'menu':
        handle_menu_command(chat_id)
    elif handler == 'chatbot':
        handle_chatbot_command(chat_id, args)
    elif handler == 'download' or handler == 'auto_download':
        handle_auto_download(chat_id, args or message_text)
    elif handler == 'dev':
        handle_dev_menu(chat_id)
    elif handler == 'checkwhatsapp':
        handle_checkwhatsapp_command(chat_id, args)
    elif handler == 'getavatar':
        handle_getavatar_command(chat_id, args)
    elif handler == 'getcontactinfo':
        handle_getcontactinfo_command(chat_id, args)
    elif handler == 'shortlink':
        handle_link_shortener(chat_id, args)
    elif handler == 'mylinks':
        handle_my_links(chat_id)
    elif handler == 'stats':
        handle_stats(chat_id, args)
    elif handler == 'alllinks':
        handle_all_links_admin(chat_id)
    elif handler == 'videoonly':
        handle_videoonly_command(chat_id, args)
    else:
        # Unknown handler - this shouldn't happen, log it
        print(f"⚠️  Internal Error: Unknown handler '{handler}'")
        send_message(chat_id, get_message("unknown_command"))
