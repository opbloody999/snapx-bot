# SnapX WhatsApp Bot

## Overview
SnapX is a professional 24/7 WhatsApp automation bot built with Python, Flask, Green API, and Turso. It provides WhatsApp automation with features such as ChatGPT integration, social media video downloading, link shortening, and a video-only mode for groups. The bot supports chat filtering to ensure it only responds to specified chats or groups, enhancing its utility within Green API's limitations. The project focuses on a modular and scalable architecture.

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
The bot uses a Flask webhook server with a single `/webhook` endpoint to process incoming WhatsApp messages. Turso database handles data persistence for user tracking, shortened links, and video-only group configurations.

The architecture is structured into three main directories:
- `core/`: Contains `main.py` (Flask server), `bot.py` (command routing), `api_requests.py` (centralized external API calls), `database.py` (Turso integration), and `logger.py` (console logging).
- `commands/`: Houses feature implementations like `chatbot.py`, `video_downloader.py`, `admin.py`, `link_shortener.py`, and `whatsapp_tools.py`.
- `config/`: Stores `commands.json` (command definitions), `messages.py` (bot responses), and `config.py` (core settings and allowed chats).

Key features and technical implementations include:
- **Centralized API Architecture**: All external API interactions (ChatGPT, video downloader, link shortener, Green API) are managed through `core/api_requests.py` for consistent handling and credential management.
- **Allowed Chats Filter**: A configurable setting in `config.py` to restrict bot responses to a maximum of three specified chats or groups, aligning with Green API limitations.
- **Single Instance Operation**: A simplified architecture utilizing one Green API instance and a single webhook endpoint.
- **Link Shortener**: Integration with the ice.bio API for URL shortening, user tracking, and click analytics, with smart URL handling to prevent conflicts with other features.
- **Video-Only Mode**: A group-specific feature designed to enable silent video downloads, streamlining media sharing in designated groups by suppressing command responses.
- **Intelligent Features**: Includes fuzzy command matching for typo tolerance, automatic video downloading for standalone URLs, greeting detection, ChatGPT auto-timeout, and smart URL handling.
- **Modular Command System**: Commands are defined in `commands.json` supporting aliases and fuzzy matching, processed by a central router.
- **Admin Commands**: Enhanced WhatsApp number checking with smart formatting and country code validation.
- **UI/UX**: Emphasizes clean WhatsApp markdown for bot responses and a declarative, JSON-based menu system.

## External Dependencies
1.  **Green API**: Primary platform for WhatsApp message handling.
2.  **Turso Database**: Cloud database for persistent data storage (user data, shortened links, video-only group settings).
3.  **ice.bio API**: Used for link shortening, user tracking, and analytics.
4.  **BatGPT ChatGPT API**: Provides conversational AI capabilities and persistent chat sessions.
5.  **BatGPT Video Downloader API**: Supports multi-platform social media video downloads (TikTok, Instagram, YouTube, Facebook, Twitter, etc.).