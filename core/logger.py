# Centralized Logging System
# Manages all console output with clean, formatted messages
# Edit console messages at the top - logging functions at the bottom

# ==================== CONSOLE MESSAGES ====================

CONSOLE_MESSAGES = {
    # ==================== INCOMING MESSAGES ====================
    'incoming_message': "📨 {sender_name} ({chat_id}): {message}",
    
    # ==================== COMMAND HANDLING ====================
    'command_found': "⚙️  {handler} | Args: {args} | Admin: {admin_only}",
    'command_blocked': "🚫 Admin command blocked: {chat_id}",
    'no_command': "➖ No command detected",
    
    # ==================== CHATGPT API ====================
    'chatgpt_request': "🤖 ChatGPT → Request sent | Chat ID: {gpt_chat_id}",
    'chatgpt_response': "✅ ChatGPT → Response received | Length: {length} chars",
    'chatgpt_error_timeout': "❌ ChatGPT → Timeout after 30s",
    'chatgpt_error_http': "❌ ChatGPT → HTTP {status_code}",
    'chatgpt_error_connection': "❌ ChatGPT → Connection failed: {error}",
    'chatgpt_error_no_response': "❌ ChatGPT → Empty response received",
    'chatgpt_error_processing': "❌ ChatGPT → Processing error: {error}",
    
    # ==================== VIDEO DOWNLOADER API ====================
    'video_request': "📥 Video Downloader → Fetching: {url}",
    'video_response': "✅ Video Downloader → Downloaded: {title}",
    'video_error_timeout': "❌ Video Downloader → Timeout after 60s",
    'video_error_http': "❌ Video Downloader → HTTP {status_code} | Response: {response_text}",
    'video_error_no_url': "❌ Video Downloader → No video URL in response | Media Info: {media_info}",
    'video_error_api_failed': "❌ Video Downloader → API returned failure | Data: {raw_data}",
    'video_error_connection': "❌ Video Downloader → Connection failed: {error}",
    'video_error_json': "❌ Video Downloader → JSON parse error: {error}",
    'video_error_processing': "❌ Video Downloader → Processing error: {error}",
    
    # ==================== LINK SHORTENER API ====================
    'link_shorten_request': "🔗 Link Shortener → Shortening: {url}",
    'link_shorten_response': "✅ Link Shortener → Created: {short_url} | ID: {link_id}",
    'link_list_request': "🔍 Link Shortener → Fetching links list",
    'link_list_response': "✅ Link Shortener → Retrieved {count} links",
    'link_stats_request': "📊 Link Stats → Fetching stats for ID: {link_id}",
    'link_stats_response': "✅ Link Stats → Retrieved stats for ID: {link_id} | Clicks: {clicks}",
    'link_error_timeout': "❌ Link Shortener → Timeout after 30s",
    'link_error_http': "❌ Link Shortener → HTTP {status_code}",
    'link_error_api': "❌ Link Shortener → API Error {error_code}: {error_message}",
    'link_error_incomplete': "❌ Link Shortener → Incomplete response | Data: {raw_data}",
    'link_error_connection': "❌ Link Shortener → Connection failed: {error}",
    'link_error_unexpected': "❌ Link Shortener → Unexpected error: {error}",
    
    # ==================== GREEN API (WHATSAPP) ====================
    'greenapi_send_message': "📤 Green API → Sending message to {chat_id}",
    'greenapi_send_file_url': "📤 Green API → Sending file (URL) to {chat_id} | File: {filename}",
    'greenapi_send_file_upload': "📤 Green API → Sending file (Upload) to {chat_id} | File: {filename}",
    'greenapi_send_poll': "📤 Green API → Sending poll to {chat_id}",
    'greenapi_send_location': "📤 Green API → Sending location to {chat_id}",
    'greenapi_send_contact': "📤 Green API → Sending contact to {chat_id}",
    'greenapi_response_success': "✅ Green API → Success | Message ID: {message_id}",
    'greenapi_response_failed': "❌ Green API → Failed to send",
    
    # ==================== DATABASE OPERATIONS ====================
    'db_link_saved': "💾 Database → Link saved | ID: {link_id} | User: ...{user}",
    'db_link_query': "🔍 Database → Querying links for user: ...{user}",
    'db_link_found': "✅ Database → Found {count} links",
    'db_reconnect': "🔄 Database → Reconnected successfully",
    'db_reconnect_error': "⚠️  Database → Reconnection failed: {error}",
    
    # ==================== CHAT INTERACTIONS ====================
    'greeting_sent': "👋 Greeted: {sender_name}",
    'gpt_activated': "🟢 ChatGPT activated: {chat_id}",
    'gpt_deactivated': "🔴 ChatGPT deactivated: {chat_id}",
    
    # ==================== IGNORED EVENTS ====================
    'ignored_self': "⏭️  Ignoring self-message",
    'ignored_not_allowed': "⏭️  Ignoring non-allowed chat: {chat_id}",
    'ignored_video_only': "⏭️  Video-only mode: Ignoring non-video in {group_id}",
    'ignored_outgoing_webhook': "⏭️  Ignoring outgoing webhook: {webhook_type}",
    
    # ==================== INITIALIZATION ====================
    'instance_init': "✅ Instance: {instance_id} | Number: {own_number}",
    'bot_ready': "🚀 WhatsApp Bot is ready!",
    'webhook_server': "📡 Webhook server running on port {port}",
    'db_init': "✅ Database connected successfully",
    'db_init_error': "⚠️  Database connection error: {error}",
    'db_not_configured': "⚠️  Database credentials not configured",
    
    # ==================== WEBHOOK EVENTS ====================
    'webhook_incoming': "📨 Webhook: incomingMessageReceived",
}


# ==================== LOGGING FUNCTIONS ====================

def log(message_key, **kwargs):
    # Main logging function - formats and prints console messages
    # Args: message_key (str) - key from CONSOLE_MESSAGES
    #       **kwargs - variables to format into message
    
    if message_key not in CONSOLE_MESSAGES:
        print(f"⚠️  Unknown log key: {message_key}")
        return
    
    message = CONSOLE_MESSAGES[message_key].format(**kwargs)
    print(message)


# ==================== INCOMING MESSAGES ====================

def log_incoming_message(sender_name, chat_id, message):
    # Log incoming WhatsApp message
    truncated = message[:50] + "..." if len(message) > 50 else message
    log('incoming_message', sender_name=sender_name, chat_id=chat_id, message=truncated)


# ==================== COMMAND HANDLING ====================

def log_command(handler, args, admin_only):
    # Log command detection and routing
    log('command_found', handler=handler, args=args, admin_only=admin_only)


def log_command_blocked(chat_id):
    # Log blocked admin command
    log('command_blocked', chat_id=chat_id)


# ==================== CHATGPT API ====================

def log_chatgpt_request(gpt_chat_id=None):
    # Log ChatGPT API request
    log('chatgpt_request', gpt_chat_id=gpt_chat_id or 'new')


def log_chatgpt_response(response_text):
    # Log ChatGPT API response
    log('chatgpt_response', length=len(response_text))


def log_chatgpt_error(error_type, **kwargs):
    # Log ChatGPT API errors
    # error_type: 'timeout', 'http', 'connection', 'no_response', 'processing'
    log(f'chatgpt_error_{error_type}', **kwargs)


# ==================== VIDEO DOWNLOADER API ====================

def log_video_request(url):
    # Log video download request (URL hidden for privacy)
    log('video_request', url='')


def log_video_response(title):
    # Log video download success (title hidden for privacy)
    log('video_response', title='')


def log_video_error(error_type, **kwargs):
    # Log video download errors
    # error_type: 'timeout', 'http', 'no_url', 'api_failed', 'connection', 'json', 'processing'
    log(f'video_error_{error_type}', **kwargs)


# ==================== LINK SHORTENER API ====================

def log_link_shorten_request(url):
    # Log link shortening request
    display_url = url[:60] + "..." if len(url) > 60 else url
    log('link_shorten_request', url=display_url)


def log_link_shorten_response(short_url, link_id):
    # Log link shortening success
    log('link_shorten_response', short_url=short_url, link_id=link_id)


def log_link_list_request():
    # Log link list fetch request
    log('link_list_request')


def log_link_list_response(count):
    # Log link list fetch success
    log('link_list_response', count=count)


def log_link_stats_request(link_id):
    # Log link stats fetch request
    log('link_stats_request', link_id=link_id)


def log_link_stats_response(link_id, clicks):
    # Log link stats fetch success
    log('link_stats_response', link_id=link_id, clicks=clicks)


def log_link_error(error_type, **kwargs):
    # Log link shortener errors
    # error_type: 'timeout', 'http', 'api', 'incomplete', 'connection', 'unexpected'
    log(f'link_error_{error_type}', **kwargs)


# ==================== GREEN API (WHATSAPP) ====================

def log_greenapi_send(operation, chat_id, **kwargs):
    # Log Green API send operations
    # operation: 'message', 'file_url', 'file_upload', 'poll', 'location', 'contact'
    short_chat = chat_id[-15:] if len(chat_id) > 15 else chat_id
    log(f'greenapi_send_{operation}', chat_id=short_chat, **kwargs)


def log_greenapi_response(success, message_id=None):
    # Log Green API response
    if success and message_id:
        log('greenapi_response_success', message_id=message_id)
    elif not success:
        log('greenapi_response_failed')


# ==================== DATABASE OPERATIONS ====================

def log_db_link_saved(link_id, user_chat_id):
    # Log database link save
    short_user = user_chat_id[-12:]
    log('db_link_saved', link_id=link_id, user=short_user)


def log_db_link_query(user_chat_id):
    # Log database link query
    short_user = user_chat_id[-12:]
    log('db_link_query', user=short_user)


def log_db_link_found(count):
    # Log database query result
    log('db_link_found', count=count)


def log_db_reconnect(success=True, error=None):
    # Log database reconnection
    if success:
        log('db_reconnect')
    else:
        log('db_reconnect_error', error=str(error))


# ==================== CHAT INTERACTIONS ====================

def log_greeting(sender_name):
    # Log greeting sent
    log('greeting_sent', sender_name=sender_name)


def log_gpt_activated(chat_id):
    # Log ChatGPT activation
    short_chat = chat_id[-15:]
    log('gpt_activated', chat_id=short_chat)


def log_gpt_deactivated(chat_id):
    # Log ChatGPT deactivation
    short_chat = chat_id[-15:]
    log('gpt_deactivated', chat_id=short_chat)


# ==================== IGNORED EVENTS ====================

def log_ignored(reason, **kwargs):
    # Log ignored messages/events
    # reason: 'self', 'not_allowed', 'video_only', 'outgoing_webhook'
    log(f'ignored_{reason}', **kwargs)


# ==================== LEGACY COMPATIBILITY ====================

def log_gpt_operation(operation, chat_id):
    # Legacy function for backward compatibility
    # Maps to new logging functions
    if operation == 'activated':
        log_gpt_activated(chat_id)
    elif operation == 'deactivated':
        log_gpt_deactivated(chat_id)


def log_video_operation(operation, **kwargs):
    # Legacy function for backward compatibility
    # No logging needed - already handled in api_requests.py
    pass


def log_link_operation(operation, **kwargs):
    # Legacy function for backward compatibility  
    # No logging needed - already handled in api_requests.py
    pass


def log_api_error(api_name, error_type, details):
    # Legacy function for backward compatibility
    # Maps to new error logging based on API type
    if 'chatgpt' in api_name.lower() or 'gpt' in api_name.lower():
        log_chatgpt_error('processing', error=str(details))
    elif 'video' in api_name.lower() or 'download' in api_name.lower():
        log_video_error('processing', error=str(details))
    elif 'link' in api_name.lower() or 'short' in api_name.lower():
        log_link_error('unexpected', error=str(details))
    else:
        # Generic error logging
        print(f"❌ API ERROR: {api_name} | {error_type} | {details}")


def log_db_operation(operation, **kwargs):
    # Legacy function for backward compatibility
    # Maps to new DB logging functions
    if operation == 'link_saved':
        log_db_link_saved(kwargs.get('link_id'), kwargs.get('user'))
    elif operation == 'link_query':
        log_db_link_query(kwargs.get('chat_id'))


# ==================== INITIALIZATION ====================

def log_initialization(instance_id=None, own_number=None, port=None):
    # Log bot initialization messages
    
    if instance_id and own_number:
        short_instance = instance_id[:6] + "..."
        log('instance_init', instance_id=short_instance, own_number=own_number)
    
    if port:
        log('webhook_server', port=port)


def log_bot_ready():
    # Log bot ready
    print("\n" + CONSOLE_MESSAGES['bot_ready'] + "\n")


def log_db_init(success=True, error=None, not_configured=False):
    # Log database initialization
    if not_configured:
        log('db_not_configured')
    elif success:
        log('db_init')
    else:
        log('db_init_error', error=str(error))


# ==================== WEBHOOK EVENTS ====================

def log_webhook(webhook_type):
    # Log webhook events (only incoming messages, ignore spam)
    if webhook_type == 'incomingMessageReceived':
        log('webhook_incoming')
    elif webhook_type in ['outgoingMessageStatus', 'outgoingAPIMessageReceived']:
        # Silently ignore these spam events - no log needed
        pass
    else:
        # Log any other unexpected webhook types for debugging
        log('ignored_outgoing_webhook', webhook_type=webhook_type)
