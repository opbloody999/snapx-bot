# SnapX WhatsApp Bot

## Overview
A professional 24/7 WhatsApp automation bot built with Python, Flask, Green API, and Turso database. Its primary purpose is to provide WhatsApp automation with features like ChatGPT integration, social media video downloading, link shortening, and a video-only mode for groups. The bot now supports chat filtering through an allowedChats configuration, ensuring it only responds to specific chats/groups within the Green API 3-chat limit. The project emphasizes a clean, modular architecture for easy maintenance and scalability.

## User Preferences
- Clean, simple folder structure - minimal nesting
- Everything organized by purpose (core, commands, config)
- # comments only (no """docstrings""")
- Green API functions centralized with simple signatures
- Easy to add new commands (just add file to commands/)
- Configuration separate from code
- Beautiful WhatsApp markdown formatting
- Beginner-friendly code structure

## System Architecture
The bot utilizes a Flask webhook server to handle incoming WhatsApp messages via a single `/webhook` endpoint. Data persistence is managed by a Turso database for user tracking, shortened links, and video-only groups.

The architecture is organized into three main folders:
- `core/`: Contains the main application logic including:
  - `main.py`: Flask webhook server
  - `bot.py`: Command routing and message handling
  - `api_requests.py`: **Centralized external API calls** (ChatGPT, video downloader, link shortener, Green API)
  - `database.py`: Turso database integration
  - `logger.py`: Console logging templates
- `commands/`: Houses feature implementations such as ChatGPT integration (`chatbot.py`), video downloading (`video_downloader.py`), admin functionalities (`admin.py`), link shortening (`link_shortener.py`), and WhatsApp tools (`whatsapp_tools.py`).
- `config/`: Stores configuration files including `commands.json` for command definitions, `messages.py` for bot responses with category organization, and `config.py` for core settings and allowed chats configuration.

Key technical implementations and features include:
- **Centralized API Architecture**: All external API calls (ChatGPT, video downloader, link shortener, Green API) are centralized in `core/api_requests.py` with clean function signatures and automatic credential management.
- **Allowed Chats Filter**: Configurable array in `config.py` to limit bot responses to specific chats/groups (max 3 per Green API limits). Empty array allows all chats.
- **Single Instance**: Simplified architecture with one Green API instance using the `/webhook` endpoint.
- **Link Shortener**: Integrates with the ice.bio API, allowing users to shorten URLs and track clicks. Smart URL handling prevents interference with video downloader.
- **Video-Only Mode**: A group-specific feature to enable silent video downloads, bypassing command responses for media-focused groups.
- **Intelligent Features**: Includes fuzzy command matching for typo tolerance, automatic video downloading upon URL detection (with link shortener exception), greeting detection, ChatGPT auto-timeout, and smart URL handling.
- **Modular Command System**: Commands are defined in `commands.json` with support for aliases and fuzzy matching, processed by a central command router.
- **Admin Commands**: Enhanced WhatsApp number checking with smart formatting (no '+' for numbers starting with 0) and better country code validation.
- **UI/UX**: Focuses on clean WhatsApp markdown formatting for bot responses and a declarative, JSON-based menu system.

## External Dependencies
1.  **Green API**: Core WhatsApp messaging platform for sending and receiving messages.
2.  **Turso Database**: Cloud database for persistent storage of user data, shortened links, and video-only group settings. Requires both `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` secrets.
3.  **ice.bio API**: Used for the link shortening feature, including URL shortening, user tracking, and click analytics.
4.  **BatGPT ChatGPT API**: Provides conversational AI capabilities with persistent chat sessions.
5.  **BatGPT Video Downloader API**: Used for multi-platform social media video downloads (TikTok, Instagram, YouTube, Facebook, Twitter, etc.).

## Configuration

### Required Secrets (Replit Secrets)
- `GREEN_API_INSTANCE_ID`: Your Green API instance ID
- `GREEN_API_TOKEN`: Your Green API token
- `TURSO_DATABASE_URL`: Turso database connection URL
- `TURSO_AUTH_TOKEN`: Turso database authentication token
- `ICE_BIO_API_KEY`: API key for ice.bio link shortener

### Allowed Chats Configuration
Edit `config/config.py` to control which chats/groups the bot responds to:
```python
ALLOWED_CHATS = [
    "923453870090",  # Individual chat (phone number without @c.us)
    "120363123456789012@g.us"  # Group chat (full group ID with @g.us)
]
```
- Maximum 3 chats/groups (Green API limit)
- Leave empty `[]` to allow all chats
- Phone numbers without @c.us suffix
- Group IDs can include or exclude @g.us suffix

### Webhook Setup
Configure webhook in Green API dashboard:
- Webhook URL: `https://your-repl-name.repl.co/webhook`
- Enable "Incoming messages" webhook type

## Recent Changes

### Logging and Webhook Fixes (November 13, 2025)
- **Disabled Flask Request Logging**: Eliminated spam from repeated `172.31.119.66 - - [timestamp] "POST /webhook HTTP/1.1" 200 -` logs by setting werkzeug logger to WARNING level
- **Line Break Separators**: Added "ㅤ" character separator between different webhook requests for clean visual spacing in console logs
- **Auto-Download Logic Fix**: Fixed bug where commands like "Short https://..." were triggering auto video download
  - Now checks if message starts with any command word (not just prefix)
  - Auto-download only triggers for standalone URLs without command words
- **Link Shortener Error Handling**: Added null check in `handle_shortener_command` to prevent NoneType errors
  - Validates result dictionary before accessing properties
  - Returns proper error message on unexpected failures
- **Webhook Error Recovery**: Changed error response from HTTP 500 to HTTP 200 with error status
  - Prevents Green API from retrying failed webhooks in infinite loops
  - Still logs full error traceback for debugging
  - Adds line break separator even on errors

### Beautiful Console Logging System (November 13, 2025)
- **Complete Logging Overhaul**: Restructured `core/logger.py` following the `config/messages.py` pattern with all log messages defined at the top in a `CONSOLE_MESSAGES` dictionary
- **Beautiful Emoji-Based Output**: All console logs now use clean, visually appealing emojis (📨, 🤖, 📥, 🔗, ✅, ❌) for different operations
- **Eliminated Logging Spam**:
  - Removed noisy webhook event logs (`outgoingAPIMessageReceived`, `outgoingMessageStatus`)
  - Made database tracking logs conditional - only logs meaningful operations (link saves/queries)
  - Removed video-only group checks from logs unless actually blocking
  - Removed excessive separator lines and bulky formatting
- **Comprehensive API Request/Response Tracking**: All external API calls now logged with:
  - ChatGPT API: Request sent, response received, errors with full details
  - Video Downloader API: Request sent, video metadata, errors
  - Link Shortener API: Request sent, shortened URL, errors
  - Green API: Message/file sending with status
- **Centralized Logging**: Updated all core files to use the new logger:
  - `core/main.py`: Clean webhook logging
  - `core/bot.py`: Command handling, greetings, ChatGPT activation
  - `core/database.py`: Conditional database operation logging
  - `core/api_requests.py`: All API request/response logging
- **Easy Customization**: All log messages editable at top of `core/logger.py` for easy maintenance
- **Legacy Compatibility**: Added compatibility functions for existing command files to prevent breaking changes
- **User-Friendly Output**: Clean, minimal logging that only shows useful information for debugging and monitoring

### Architecture Refactoring: API Centralization (November 13, 2025)
- **Major Refactor**: Centralized all external API calls into `core/api_requests.py`
- **Removed `core/green_api.py`**: All Green API functionality migrated to `api_requests.py` with cleaner function signatures
- **API Functions Centralized**:
  - ChatGPT API (BatGPT)
  - Video Downloader API (BatGPT)
  - Link Shortener API (ice.bio)
  - Green API (WhatsApp) - all endpoints
- **Credential Management**: Green API credentials now managed internally - callers don't need to pass `instance_id` and `token`
- **Clean Function Signatures**: 
  - Before: `greenapi_send_message_request(instance_id, token, chat_id, text)`
  - After: `greenapi_send_message(chat_id, text)`
- **Category Organization**: All API files now organized with clear category headers:
  - `core/api_requests.py`: ChatGPT, Video Downloader, Link Shortener, Green API sections
  - `config/messages.py`: Main & Menu, ChatGPT, Video Downloader, Link Shortener, Admin, WhatsApp Tools sections
- **Logger Infrastructure**: Created `core/logger.py` with predefined console message templates for consistent, clean logging
- **Benefits**:
  - Single source of truth for all external API integrations
  - Easier to maintain and debug API calls
  - Consistent error handling across all APIs
  - Thread-safe credential management
  - Better code organization and separation of concerns
- **Production Tested**: All features verified working (menu, greeting, link shortener with password, mylinks, ChatGPT chat, all commands functional)

### Link Shortener Password Display Feature (November 13, 2025)
- **Password Field Support**: Link shortener now displays passwords in both success messages and .mylinks list
- Added `password` column to `shortened_links` table in database
- Removed `created_at` column from database (ice.bio API already tracks this)
- Updated ice.bio API requests to include `"channel": 1` parameter
- Success message now shows actual password value: `🔒 *Password:* yourpassword` instead of just "Password Protected: Yes"
- `.mylinks` command now displays password for each link if user set one
- Database functions updated:
  - `save_shortened_link` now accepts and saves password parameter
  - `get_user_link_ids` returns dict mapping link_id to password
  - Fixed `get_all_link_ids` to use `ORDER BY id DESC` instead of removed `created_at`
- All changes maintain backward compatibility with existing links without passwords

### Database Schema Fix (November 12, 2025)
- **CRITICAL FIX**: Fixed `link_id` data type from INTEGER to TEXT in `shortened_links` table
- This was causing all link shortener lookups to fail silently
- Removed automatic table creation on bot startup (was recreating broken tables)
- Database tables now created manually with correct schema:
  - `users`: Tracks user interactions (chat_id, message_count, timestamps)
  - `shortened_links`: Stores link IDs as TEXT (user_chat_id, link_id, created_at)
  - `video_only_groups`: Groups with video-only mode enabled
- Updated database functions to ensure type consistency (convert link_id to string)
- Added type hints to fix LSP warnings for `libsql_experimental` library
- **Connection Retry Logic**: Added automatic reconnection to handle Turso stream expiration
  - Reuses global connection instead of creating new connections per query
  - Automatically reconnects only when "stream not found" errors occur
  - All write operations now properly commit changes to Turso cloud
  - Ensures reliable database access and data persistence even after idle periods

### Database Library Upgrade (November 2024)
- Upgraded from archived `libsql-client` to official `libsql-experimental` package
- Fixed 505 connection errors with Turso database
- Removed `instances` table (no longer needed with single-instance architecture)
- Database now only tracks: users, shortened_links, and video_only_groups
- Split `TURSO_DATABASE_URL` secret into two separate secrets:
  - `TURSO_DATABASE_URL`: Contains only the database URL (libsql://...)
  - `TURSO_AUTH_TOKEN`: Contains the authentication token
- Database is now properly initialized and used for user tracking, link shortening, and video-only mode

### Single Instance Architecture
- Removed multi-instance support for simplicity
- Now uses single `/webhook` endpoint instead of `/webhook1`, `/webhook2`, etc.
- Single Green API instance configured via `GREEN_API_INSTANCE_ID` and `GREEN_API_TOKEN`

### Allowed Chats Feature
- Added `ALLOWED_CHATS` array in `config/config.py`
- Bot now filters incoming messages to only respond to allowed chats/groups
- Supports up to 3 chats (Green API limit)
- Can mix individual chats and groups
- Empty array allows all chats

### CheckWhatsApp Command Improvements
- Fixed number formatting: No '+' prefix for numbers starting with 0
- Added validation for numbers starting with 0 that aren't 11 digits
- Better error messages suggesting country code inclusion
- Example: `.checkwa 03001234567` shows "03001234567" not "+923001234567"

### Link Shortener Fix
- Fixed interference with video downloader
- Commands like `.short <url>` no longer trigger video download
- URL detection now checks if message starts with command prefix
- Prevents auto-download when explicitly using link shortener commands