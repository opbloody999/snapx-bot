# SnapX Bot - User Guide

Welcome to SnapX Bot! This guide will help you use all available features.

## 📱 Getting Started

### First Steps
1. Add the bot's WhatsApp number to your contacts
2. Send a message: `Hi` or `Hello`
3. You'll receive a welcome message with instructions

### Command Structure
- All commands start with a dot (`.`)
- Commands are **case-insensitive** (`.MENU` = `.menu` = `.Menu`)
- Many commands have shortcuts to save typing
- Example: `.download` = `.dl`

---

## 🎯 Available Commands

### 📥 Video Downloader

**Download videos from social media platforms**

```
.download <url>
.dl <url>
```

**Supported Platforms:**
- TikTok
- Instagram (Reels, Posts, Stories)
- YouTube (Videos, Shorts)
- Facebook
- Twitter/X
- And many more!

**Examples:**
```
.download https://www.tiktok.com/@username/video/1234567890
.dl https://www.instagram.com/reel/ABC123/
.dl https://youtube.com/watch?v=dQw4w9WgXcQ
```

**How it works:**
1. Send the command with a video URL
2. Bot downloads the video
3. Video is sent directly to your chat
4. If auto-send fails, you'll get a direct download link

---

### 🤖 ChatGPT Mode

**Chat with AI powered by ChatGPT**

**Activate ChatGPT:**
```
.chatgpt on
.gpt on
```

**Deactivate ChatGPT:**
```
.chatbot off
.gpt off
```

**How it works:**
1. Type `.chatgpt on` to activate
2. **All your messages** will be sent to ChatGPT
3. No other commands work while active
4. ChatGPT remembers your conversation
5. Type `.chatgpt off` to deactivate and return to normal mode

**Example Conversation:**
```
You: .gpt on
Bot: 🤖 ChatGPT Mode Activated!

You: What's the capital of France?
Bot: The capital of France is Paris...

You: Tell me more about it
Bot: Paris is known for...

You: .gpt off
Bot: ✅ ChatGPT mode deactivated!
     [Shows main menu]
```

---

### ℹ️ Info & Help Commands

**Show main menu:**
```
.menu
```

**Get detailed help:**
```
.help
```

**Show welcome message:**
```
Hi
Hello
```

---

## ⚡ Command Shortcuts

Save time with shortcuts! Here are the available shortcuts:

| Full Command | Shortcut | What it does |
|-------------|----------|--------------|
| `.download` | `.dl` | Download video |
| `.chatgpt` | `.gpt` | Toggle ChatGPT mode |
| `.help` | `.menu` | Get help / Shows Menu |

**Custom Shortcuts:**
You can customize shortcuts by editing `app/config/shortcuts.json` in the project files.

---

## 🎯 Usage Tips

### Best Practices
1. ✅ **Use shortcuts** to save typing (`.dl` instead of `.download`)
2. ✅ **Check the menu** if you forget a command (`.m`)
3. ✅ **Use ChatGPT mode** for conversations, then deactivate when done
4. ✅ **Copy video URLs directly** from your browser or app

---

## 🆘 Troubleshooting

### Video Download Issues
**Problem:** "Failed to download video"

**Solutions:**
- ✅ Check if the video is **public** (not private)
- ✅ Make sure the URL is **complete**
- ✅ Try copying the URL again
- ✅ Check if the platform is supported

### ChatGPT Issues
**Problem:** "Request timed out"

**Solutions:**
- ✅ Wait a moment and try again
- ✅ Keep messages reasonably short
- ✅ Deactivate and reactivate if stuck

### Commands Not Working
**Problem:** Bot doesn't respond

**Solutions:**
- ✅ Make sure you're using the dot (`.`) prefix
- ✅ Check if ChatGPT mode is active (deactivate if needed)
- ✅ Try using the shortcut version
- ✅ Type `.menu` to see available commands

---

## 📞 Support

If you encounter issues:
1. Contact the bot administrator

---

## 🔮 Coming Soon

More features will be added based on user feedback!
Stay tuned for updates! 🚀

---

**Last Updated:** November 11, 2025  
**Version:** 2.0
