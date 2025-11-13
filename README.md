# SnapX WhatsApp Bot

A professional WhatsApp automation bot built with Python, Flask, and Green API. Features ChatGPT integration, social media video downloader, and clean modular architecture for easy expansion.

## 🌟 Features

### Core Features
- 🤖 **ChatGPT Integration** - Conversational AI with persistent chat sessions
- 📥 **Video Downloader** - Download videos from TikTok, Instagram, YouTube, and more
- 📋 **Declarative Menu System** - Easily customizable without touching code
- ⚡ **Command Shortcuts** - Auto-generated, editable shortcuts for all commands
- 📞 **Phone Number Filtering** - Respond to all incoming, specific number for outgoing

### Technical Features
- 24/7 webhook-based message handling
- Clean 3-folder architecture: core, commands, config
- Centralized Green API integration
- State management for ChatGPT sessions
- Error handling and logging throughout
- Extensible command routing system

## 📁 Project Structure

```
.
├── run.py                          # Entry point
├── requirements.txt                # Python dependencies
│
├── core/                           # Main application code
│   ├── main.py                     # Flask webhook server
│   ├── bot.py                      # Command routing and handlers
│   └── green_api.py                # WhatsApp API functions
│
├── commands/                       # Command implementations
│   ├── chatbot.py                  # ChatGPT integration
│   └── video_downloader.py         # Video download logic
│
└── config/                         # Configuration files
    ├── messages.py                 # Bot response messages
    ├── config.py                   # Core settings
    ├── shortcuts.json              # Command shortcuts (editable)
    └── menu_config.json            # Menu structure (editable)
```

## 🚀 Setup

### Prerequisites
- Python 3.11+
- Green API account ([sign up here](https://green-api.com))
- Replit account (for hosting)

### Installation

1. **Clone or fork this repository**

2. **Set up Green API:**
   - Sign up at [green-api.com](https://green-api.com)
   - Create a new instance
   - Copy your Instance ID and API Token

3. **Configure Replit Secrets:**
   Add these environment variables in Replit Secrets:
   ```
   GREEN_API_INSTANCE_ID=your_instance_id
   GREEN_API_TOKEN=your_api_token
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure webhook in Green API dashboard:**
   - Go to your Green API dashboard
   - Set webhook URL to: `https://your-repl.repl.co/webhook`
   - Enable "Incoming messages" webhook

6. **Run the bot:**
   ```bash
   python run.py
   ```

## 🎯 Usage

### For Users
See [USER_GUIDE.md](USER_GUIDE.md) for complete user documentation.

**Quick Start:**
```
.start          - Start the bot
.menu           - Show all commands
.help           - Get help

.dl <url> - Download social media videos
.gpt on     - Activate ChatGPT mode
.gpt off    - Deactivate ChatGPT
```

### For Developers

#### Adding New Commands

1. **Create command file in `commands/` folder:**
```python
# commands/myfeature.py

def handle_mycommand(args):
    # Your logic here
    return "Response message"
```

2. **Import and add to router in `core/bot.py`:**
```python
# Import your command
from commands.myfeature import handle_mycommand

# Add to handle_incoming_message function
elif command == "mycommand":
    result = handle_mycommand(args)
    send_message(chat_id, result)
```

3. **Add to menu config in `config/menu_config.json`:**
```json
{
  "command": ".mycommand <args>",
  "shortcut": ".mc",
  "description": "Does something cool"
}
```

4. **Add shortcut in `config/shortcuts.json`:**
```json
"shortcuts": {
  "mc": "mycommand"
}
```

#### Using Green API Functions

All WhatsApp API functions are in `core/green_api.py`:

```python
from core.green_api import send_message, send_file_by_url, send_poll

# Send text message
send_message(chat_id, "Hello!")

# Send video/file from URL
send_file_by_url(chat_id, video_url, "video.mp4", "Check this out")

# Send poll
options = [{"optionName": "Yes"}, {"optionName": "No"}]
send_poll(chat_id, "Do you agree?", options)
```

For complete API documentation, visit: https://green-api.com/en/docs/

#### Project Configuration

**Environment Variables:**
- `GREEN_API_INSTANCE_ID` - Your Green API instance ID
- `GREEN_API_TOKEN` - Your Green API token
- `PORT` - Server port (default: 5000)

**Config Files:**
- `config/messages.py` - All bot response messages
- `config/config.py` - Command prefix and settings
- `config/shortcuts.json` - Command shortcuts
- `config/menu_config.json` - Menu structure

## 🏗️ Architecture

### Simple 3-Folder Design

The bot follows a clean, beginner-friendly structure:

1. **core/** - Main application logic
   - `main.py` - Flask server and webhook handling
   - `bot.py` - Command routing and message handling
   - `green_api.py` - WhatsApp API integration

2. **commands/** - Feature implementations (NO subfolders)
   - Each command gets its own file
   - Easy to add new features
   - Simple imports

3. **config/** - All configuration
   - Messages, settings, shortcuts, menus
   - Edit without touching main code
   - JSON for easy customization

### Why This Structure?

- **Minimal folders** - No excessive nesting
- **Clear separation** - Each folder has one purpose
- **Easy to extend** - Just add a file to commands/
- **Beginner friendly** - Simple to understand and modify
- **Centralized API** - All Green API code in one place

## 🔧 Customization

### Changing Bot Messages

Edit `config/messages.py`:
```python
MESSAGES = {
    "welcome": "Your custom welcome message",
    "video_downloader_help": "Your custom help text"
}
```

### Adding Command Shortcuts

Edit `config/shortcuts.json`:
```json
{
  "shortcuts": {
    "dl": "download",
    "your_shortcut": "your_command"
  }
}
```

### Customizing Menu

Edit `config/menu_config.json` to change menu structure, categories, and commands.

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues or questions:
- Green API Documentation: https://green-api.com/en/docs/
- Create an issue in this repository
