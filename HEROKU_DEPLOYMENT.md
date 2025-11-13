# 🚀 Heroku Deployment Guide for WhatsApp Bot

This guide will help you deploy your WhatsApp bot to Heroku successfully.

## 📋 What Was Fixed

Your bot now includes all the necessary files for Heroku deployment:

1. **Procfile** - Tells Heroku how to run your app using Gunicorn (production server)
2. **requirements.txt** - Cleaned up and includes Gunicorn
3. **runtime.txt** - Specifies Python 3.11.13
4. **Updated .gitignore** - Prevents unnecessary files from being deployed

## 🔧 Deployment Steps

### Step 1: Push Changes to GitHub

Since you're deploying from a GitHub repo, commit and push these new files:

```bash
git add Procfile requirements.txt runtime.txt .gitignore HEROKU_DEPLOYMENT.md
git commit -m "Add Heroku deployment configuration"
git push origin main
```

### Step 2: Set Environment Variables on Heroku

Your bot requires these environment variables. Go to your Heroku dashboard:

1. Open your app: https://dashboard.heroku.com/apps/snapx-bot
2. Click **Settings** tab
3. Click **Reveal Config Vars**
4. Add the following variables:

**Required (bot won't start without these):**
- `GREEN_API_INSTANCE_ID` = Your Green API instance ID
- `GREEN_API_TOKEN` = Your Green API token
- `PORT` = 5000 (Heroku sets this automatically, but you can verify)

**Optional (for additional features):**
- `TURSO_DATABASE_URL` = Your database URL (if using database)
- `TURSO_AUTH_TOKEN` = Your database auth token (if using database)
- `ICE_BIO_API_KEY` = Your link shortener API key (if using link shortening)

### Step 3: Deploy from GitHub

Since your app is connected to GitHub:

1. Go to your app's **Deploy** tab
2. Scroll to **Manual deploy** section
3. Select your branch (usually `main`)
4. Click **Deploy Branch**
5. Wait for the build to complete

### Step 4: Check Logs

After deployment, check if the bot is running:

**Option 1: Using Heroku CLI (Recommended)**

Install Heroku CLI if you haven't:
- Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
- Mac: `brew tap heroku/brew && brew install heroku`
- Linux: `curl https://cli-assets.heroku.com/install.sh | sh`

Then login and view logs:
```bash
heroku login
heroku logs --tail --app snapx-bot
```

**Option 2: Using Heroku Dashboard**
1. Go to your app
2. Click **More** → **View logs**

### Step 5: Verify It's Working

You should see in the logs:
```
🤖 WhatsApp Automation Bot Starting...
✅ Instance initialized successfully
🚀 Bot is ready to receive messages!
📡 Webhook server running on port 5000
```

If you see this, your bot is running! ✅

## 🐛 Troubleshooting

### Error: "No web processes running" (H14)
- **Cause:** Missing Procfile or wrong format
- **Fix:** This is now fixed with the Procfile we created

### Error: "Application error" 
- **Cause:** Missing environment variables
- **Fix:** Make sure you set `GREEN_API_INSTANCE_ID` and `GREEN_API_TOKEN` in Config Vars

### Error: "ModuleNotFoundError"
- **Cause:** Missing dependencies in requirements.txt
- **Fix:** The requirements.txt has been cleaned and includes all dependencies

### Bot starts but crashes immediately
- **Cause:** Green API credentials not set or invalid
- **Fix:** Double-check your Config Vars on Heroku Settings

## 📊 View Real-Time Logs

To see the same console output you see on Replit:

```bash
# See live streaming logs (like Replit console)
heroku logs --tail --app snapx-bot

# See only your app's logs (not Heroku system logs)
heroku logs --tail --source app --app snapx-bot

# See last 500 lines
heroku logs -n 500 --app snapx-bot

# Search for errors
heroku logs -n 1000 --app snapx-bot | grep ERROR
```

## 🎯 Quick Reference

**Your App URL:** https://snapx-bot-df1a22f37988.herokuapp.com
**Webhook URL:** https://snapx-bot-df1a22f37988.herokuapp.com/webhook

**Important Commands:**
```bash
# View logs
heroku logs --tail --app snapx-bot

# Restart app
heroku restart --app snapx-bot

# Check app status
heroku ps --app snapx-bot

# Open app in browser
heroku open --app snapx-bot

# Set environment variable
heroku config:set VARIABLE_NAME=value --app snapx-bot
```

## ✅ Deployment Checklist

- [ ] Procfile created ✅
- [ ] requirements.txt updated with Gunicorn ✅
- [ ] runtime.txt created ✅
- [ ] Changes pushed to GitHub
- [ ] Environment variables set on Heroku
- [ ] App deployed from GitHub
- [ ] Logs checked and bot is running
- [ ] Webhook URL configured in Green API dashboard

## 🔗 Next Steps

1. Push the changes to GitHub
2. Set your Config Vars (especially GREEN_API credentials)
3. Deploy from GitHub
4. Check logs to confirm it's running
5. Update your Green API webhook URL to: `https://snapx-bot-df1a22f37988.herokuapp.com/webhook`

Your bot is now Heroku-ready! 🎉
