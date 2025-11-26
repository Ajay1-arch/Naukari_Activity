# Telegram Notifications Setup Guide

This guide will help you set up Telegram notifications for the Naukri Automation scheduler. You'll receive real-time updates about every automation run directly on your phone!

## Prerequisites

- Telegram app installed on your phone or desktop
- Access to Telegram's BotFather service
- Your Telegram account

## Step-by-Step Setup

### Step 1: Create a Telegram Bot

1. **Open Telegram** and search for **@BotFather**
2. **Start the conversation** by clicking `/start`
3. **Create a new bot** by typing `/newbot`
4. **Follow the prompts:**
   - Give your bot a name (e.g., "Naukri Automation Bot")
   - Give your bot a username (must end with "bot", e.g., "naukri_automation_bot_2025")

5. **Copy your Bot Token** - it looks like: `123456789:ABCDEFGHIJKLMNOPQRSTuvwxyz`
   - Save this securely, you'll need it soon!

### Step 2: Get Your Chat ID

You can get your chat ID in two ways:

#### Method A: Direct Message to Your Bot (Recommended)

1. **Search for your newly created bot** (the username you just created)
2. **Send a message** to the bot (any message, like `/start`)
3. **Visit this URL** in your browser (replace `YOUR_BOT_TOKEN` with the token from Step 1):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
4. **Find your Chat ID** in the response. Look for the `"chat":{"id":XXXXX}` section
   - Example: If you see `"id":123456789`, your chat ID is `123456789`

#### Method B: Using @userinfobot

1. **Search for @userinfobot** in Telegram
2. **Send any message** to it
3. **It will reply with your ID** in the format: `Your ID: 123456789`

### Step 3: Update Your Secrets File

Open `.secrets/secrets.json` in your project directory and update the Telegram section:

```json
{
  "naukri": {
    "username": "your_email@gmail.com",
    "password": "your_password",
    "mobile": "9999999999"
  },
  "paths": {
    "original_resume": "C:\\path\\to\\resume.pdf",
    "modified_resume": "C:\\path\\to\\modified_resume.pdf"
  },
  "chrome": {
    "headless": false
  },
  "telegram": {
    "bot_token": "YOUR_BOT_TOKEN_HERE",
    "chat_id": "YOUR_CHAT_ID_HERE"
  }
}
```

Replace:
- `YOUR_BOT_TOKEN_HERE` with your bot token from Step 1
- `YOUR_CHAT_ID_HERE` with your chat ID from Step 2

### Step 4: Test Your Setup

1. **Start the scheduler:**
   ```powershell
   python src/scheduler.py
   ```

2. **Check Telegram** - You should receive:
   - ✅ Startup notification when scheduler starts
   - ✅ Success/failure notifications after each run
   - ✅ Status updates with run statistics

## What You'll Receive

### Startup Notification
```
🚀 Naukri Automation Started

The scheduler is now running and will execute every 1.5 hours

✅ All systems ready
⏰ Next run in ~90 minutes
```

### Success Notification
```
✅ Naukri Automation Successful

Run #: 1
Timestamp: 2025-11-26 12:00:00

Profile updated and resume uploaded

Tasks Completed:
• ✅ Naukri Login
• ✅ Profile Update
• ✅ Resume Upload
• ✅ Logout

⏰ Next run scheduled in ~90 minutes
```

### Failure Notification
```
❌ Naukri Automation Failed

Run #: 1
Timestamp: 2025-11-26 12:00:00

Error:
[Error message details]

⚠️ Please check logs at:
logs/naukri.log

⏰ Will retry in ~90 minutes
```

## Troubleshooting

### Not Receiving Notifications?

1. **Verify Bot Token:**
   - Check `.secrets/secrets.json` for typos
   - Ensure token is copied completely

2. **Verify Chat ID:**
   - Make sure you got the correct Chat ID
   - Common mistake: Using username instead of ID (must be numbers only)

3. **Check Network:**
   - Ensure your computer has internet access
   - The script needs to reach `api.telegram.org`

4. **Review Logs:**
   ```powershell
   cat logs/naukri.log
   ```
   - Look for Telegram-related error messages
   - If you see "Telegram notifications disabled", check your secrets file

### Example Error Messages

| Error | Solution |
|-------|----------|
| `Missing bot_token or chat_id` | Update `.secrets/secrets.json` with both values |
| `Failed to send Telegram message` | Check internet connection |
| `401 Unauthorized` | Bot token is incorrect |
| `Bad Request: chat not found` | Chat ID is incorrect |

## Security Notes

⚠️ **Important:**
- Never share your bot token or chat ID with anyone
- The `.secrets/secrets.json` file is already in `.gitignore` to prevent accidental commits
- Keep your secrets file private and secure

## Disabling Notifications

If you want to temporarily disable Telegram notifications:
- Remove the bot token and chat ID values from `.secrets/secrets.json`
- The notifier will gracefully disable itself and continue running the scheduler

## Advanced: Creating a Channel for Notifications

For production setups, you might want notifications in a dedicated channel:

1. **Create a Telegram channel** (private or public)
2. **Add your bot** to the channel as an administrator
3. **Get the channel ID** (usually `-100XXXXXXXXXXX`)
4. **Update your `.secrets/secrets.json`** with the channel ID instead of your personal chat ID

## Support

If you need help:
1. Check the `logs/naukri.log` file for detailed error messages
2. Verify your bot token at: https://api.telegram.org/botYOUR_TOKEN/getMe
3. Review the Telegram Bot API documentation: https://core.telegram.org/bots/api

---

**Setup Complete!** 🎉 You should now receive all Naukri automation notifications on Telegram.
