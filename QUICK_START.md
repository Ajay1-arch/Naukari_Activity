# Quick Start Guide - 5 Minutes to Setup

## Step 1: Setup (2 minutes)

```bash
cd naukri-automation
python setup.py
```

Follow the prompts:
- Enter your Naukri email
- Enter your Naukri password  
- Enter your mobile number
- Enter path to your resume PDF
- Confirm Chrome settings

## Step 2: Test Run (1 minute)

```bash
python src/naukri_main.py
```

Watch the browser open, log in, and upload your resume. Check console for "Successful" message.

## Step 3: Schedule (2 minutes)

Choose one:

**Option A: Run Every Hour (Recommended)**
```bash
python src/scheduler.py
```

**Option B: Windows Task Scheduler (Best)**
1. Open Task Scheduler
2. Create new task
3. Set trigger: Daily/Hourly
4. Set action: Run `naukri-automation\run_once.bat`

**Option C: Quick Command**
```powershell
# Every hour at :00
schtasks /create /tn "Naukri Automation" /tr "C:\path\to\naukri-automation\run_once.bat" /sc hourly
```

## Done! ✅

Your script will now:
- Run automatically on schedule
- Upload your resume
- Update your profile
- Rotate your headline
- Log everything to `logs/naukri.log`

## Check Logs

```bash
# View last 20 lines
tail -20 logs/naukri.log
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Login fails | Verify email/password in `.secrets/secrets.json` |
| Resume not found | Check file path in `.secrets/secrets.json` |
| Chrome won't open | Install Chrome if missing |
| Task runs but nothing happens | Check `logs/naukri.log` for errors |

## Files Explained

| File | Purpose |
|------|---------|
| `.secrets/secrets.json` | Your credentials (keep private!) |
| `config/config.ini` | Script settings |
| `src/naukri_main.py` | Main automation script |
| `src/scheduler.py` | Runs script on schedule |
| `logs/naukri.log` | Execution logs |

## Next Steps

- Read full `README.md` for advanced options
- Customize headlines in `src/naukri_main.py`
- Adjust schedule in `config/config.ini`
- Monitor logs regularly

---

**You're all set! Your Naukri profile will now update automatically! 🎉**
