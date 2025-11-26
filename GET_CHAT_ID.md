# Get Your Telegram Chat ID

## Quick Method - Using Browser

1. **Open your browser** and visit this URL:
```
https://api.telegram.org/bot8105905127:AAHoBpI0Df-xi4WOevJc0TZrahn5oBv0VV0/getUpdates
```

2. **If you haven't messaged the bot yet:**
   - Open Telegram
   - Search for your bot name (the one you created)
   - Send any message (like `/start`)
   - Wait 2-3 seconds

3. **Refresh the browser page** (the URL from step 1)

4. **Look for your Chat ID** in the JSON response:
   - Find `"chat":{"id":XXXXXXXXX}` 
   - Your Chat ID is that number (e.g., `123456789`)

## Alternative Method - Using PowerShell

Run this command (your bot token is already included):

```powershell
$token = "8105905127:AAHoBpI0Df-xi4WOevJc0TZrahn5oBv0VV0"
$url = "https://api.telegram.org/bot$token/getUpdates"
(Invoke-WebRequest -Uri $url).Content | ConvertFrom-Json | ConvertTo-Json
```

This will show you the JSON response with your Chat ID.

## Update Your Secrets

Once you have your Chat ID (a number like 123456789), edit:
`.secrets/secrets.json`

Change this line:
```json
"chat_id": "YOUR_CHAT_ID_HERE"
```

To:
```json
"chat_id": "YOUR_ACTUAL_CHAT_ID_NUMBER"
```

Example:
```json
"chat_id": "123456789"
```

## Test It Works

After updating, run:
```powershell
cd c:\Users\AJAY\Downloads\naukri-automation
python src/scheduler.py
```

Check your Telegram for a startup notification! 🚀
