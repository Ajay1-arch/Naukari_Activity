# Telegram Notifications - Quick Start

## TL;DR Setup (5 minutes)

### 1️⃣ Get Bot Token
- Open Telegram → Search **@BotFather**
- Send `/newbot`
- Follow prompts, get your token (looks like: `123456789:ABCDEFGHIJKLMNOPQRSTuvwxyz`)

### 2️⃣ Get Chat ID
- Message your bot (send any text)
- Visit in browser: `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates`
- Find `"id":XXXXX` → That's your chat ID

### 3️⃣ Update Secrets
Edit `.secrets/secrets.json`:
```json
"telegram": {
  "bot_token": "YOUR_BOT_TOKEN_HERE",
  "chat_id": "YOUR_CHAT_ID_HERE"
}
```

### 4️⃣ Done! ✅
Run scheduler and check Telegram for notifications:
```powershell
python src/scheduler.py
```

## What You'll Get

Every scheduler run sends you:
- 🚀 **Startup** - Scheduler started, ready to run
- ✅ **Success** - Run completed with details
- ❌ **Failure** - Error alerts with logs location
- 📊 **Summary** - Statistics after each run

## Detailed Setup

See [TELEGRAM_SETUP.md](./TELEGRAM_SETUP.md) for complete guide with:
- Screenshots
- Troubleshooting
- Advanced options (channels, etc)

## Test It

```powershell
cd c:\Users\AJAY\Downloads\naukri-automation
python src/scheduler.py
```

Check your Telegram in 5 seconds for startup notification! 📱
