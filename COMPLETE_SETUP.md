# Complete Naukri Automation Setup Guide

## 🎯 What You Have

A fully automated Naukri profile updater that:
- ✅ Logs in to your Naukri account
- ✅ Uploads your resume (with timestamp for freshness)
- ✅ Updates your profile headline to attract recruiters
- ✅ Runs automatically every 1.5 hours with random variance
- ✅ Tracks all progress and statistics
- ✅ Provides real-time dashboard
- ✅ Stores credentials securely (never on GitHub)
- ✅ Version controlled on GitHub

## 📋 Complete Setup (5 Minutes)

### Step 1: Verify Installation
```powershell
cd c:\Users\AJAY\Downloads\naukri-automation
python verify_setup.py
```

You should see:
```
✓ Project structure is correct
✓ All required files are present
✓ Configuration files exist
✓ Logging directories ready
```

### Step 2: Configure Your Credentials
```powershell
python setup.py
```

You'll be prompted for:
1. **Naukri Email**: Your login email
2. **Naukri Password**: Your login password
3. **Mobile Number**: Your registered mobile
4. **Resume Path**: Full path to your resume file
   - Example: `C:\Users\AJAY\Documents\Resume.pdf`

This creates `.secrets/secrets.json` (protected from Git).

### Step 3: Test the Script
```powershell
run_once.bat
```

Expected output:
```
Starting Naukri Automation...
Logging in to Naukri...
[✓] Successfully logged in
Uploading resume...
[✓] Resume uploaded successfully
Updating profile headline...
[✓] Headline updated: "Data Engineer | GCP | Python"
Logging out...
[✓] Successfully logged out

Execution completed successfully in 47.3 seconds
```

### Step 4: Start the Scheduler
```powershell
run_scheduler.bat
```

Expected output:
```
╔════════════════════════════════════════╗
║  NAUKRI AUTOMATION SCHEDULER STARTED   ║
║  Frequency: 1.5 hours (with variance)  ║
║  Progress: logs/progress.json          ║
║  Logs: logs/naukri.log                 ║
╚════════════════════════════════════════╝

Tip: To view progress, run: view_progress.bat
Tip: Press Ctrl+C to stop the scheduler

[Run #1] Starting Naukri automation script...
[Run #1] Script completed successfully in 47.3 seconds
Next run scheduled for: 2025-11-26 14:15:30 (88.5 minutes from now)
Waiting 5310 seconds (88.5 minutes)...
```

### Step 5: Monitor Progress (Optional Terminal)
In a new terminal window:
```powershell
view_progress.bat
```

Shows:
```
SCHEDULER PROGRESS SUMMARY
============================================================
Total Runs:           1
Successful:           1
Failed:               0
Success Rate:         100.0%
Last Run Status:      SUCCESS
```

## 🕐 How Scheduling Works

### Execution Timeline

```
Time       Event
─────────────────────────────────────────────
00:00      First run starts
00:47      First run completes (47s duration)
02:35      Second run starts (1h 48m after first)
03:22      Second run completes
05:00      Third run starts (1h 38m after second)
...
```

### Why Random Timing?

The scheduler uses **random delays between 75-105 minutes** (instead of fixed 90 minutes):

- **Looks Natural**: Naukri doesn't see a pattern
- **Avoids Detection**: Less likely to trigger automated systems
- **Still Frequent**: Average 1.5 hours = ~16 updates per day
- **Visibility**: Your profile stays fresh for recruiters

### Configuration Details

File: `config/config.ini`

```ini
[Scheduling]
RANDOM_DELAY_MIN = 4500    # 75 minutes (minimum wait)
RANDOM_DELAY_MAX = 6300    # 105 minutes (maximum wait)
USE_RANDOM_TIMES = True    # Enable randomness
```

## 📊 Monitoring Dashboard

### Instant Progress Check
```powershell
view_progress.bat
```

### Sample Output
```
╔══════════════════════════════════════════════════════════╗
║     NAUKRI AUTOMATION - SCHEDULER DASHBOARD              ║
╚══════════════════════════════════════════════════════════╝

SCHEDULER PROGRESS SUMMARY
============================================================
Total Runs:           25
Successful:           24
Failed:               1
Success Rate:         96.0%
Last Run Status:      SUCCESS
Last Run Time:        2025-11-26 15:30:45
Scheduler Started:    2025-11-26 10:00:00
============================================================

RECENT RUNS (Last 15)
────────────────────────────────────────────────────────────
Run # │ Timestamp           │ Status      │ Duration │ Error
    1 │ 2025-11-26 10:00:15 │ ✓ SUCCESS   │ 47.2s    │ -
    2 │ 2025-11-26 11:52:30 │ ✓ SUCCESS   │ 48.1s    │ -
    3 │ 2025-11-26 13:42:15 │ ✗ FAILED    │ 12.5s    │ TimeoutError
    ...
────────────────────────────────────────────────────────────

DETAILED STATISTICS
────────────────────────────────────────────────────────────
Average Run Duration: 47.5 seconds
Minimum Duration:     12.5 seconds
Maximum Duration:     52.8 seconds
Total Run Time:       1187.5 seconds (0.33 hours)
────────────────────────────────────────────────────────────
```

## 📁 Log Files Location

### Main Logs
- **File**: `logs/naukri.log`
- **Purpose**: Detailed execution information
- **Size**: Auto-rotated at 10MB

### Progress Statistics
- **File**: `logs/progress.json`
- **Format**: JSON with all run details
- **Use**: Dashboard reads this for statistics

## 🔄 Daily Usage

### Morning: Check Status
```powershell
view_progress.bat
```

### Throughout Day: Let it Run
The scheduler runs in the background automatically

### Evening: Review Performance
```powershell
type logs\naukri.log | tail -100  # Last 100 lines
```

### If Issues Occur
Check the full log:
```powershell
Get-Content logs\naukri.log -Tail 200
```

## ⚙️ Customization Options

### Change Update Frequency

**To 2 Hours:**
Edit `config/config.ini`:
```ini
RANDOM_DELAY_MIN = 6300    # 105 minutes
RANDOM_DELAY_MAX = 7500    # 125 minutes
SCHEDULE_INTERVAL_HOURS = 2.0
```

**To 1 Hour:**
```ini
RANDOM_DELAY_MIN = 3300    # 55 minutes
RANDOM_DELAY_MAX = 3900    # 65 minutes
SCHEDULE_INTERVAL_HOURS = 1.0
```

**To 30 Minutes:**
```ini
RANDOM_DELAY_MIN = 1500    # 25 minutes
RANDOM_DELAY_MAX = 1800    # 30 minutes
SCHEDULE_INTERVAL_HOURS = 0.5
```

Then restart the scheduler for changes to take effect.

### Disable Features

**Skip Resume Upload** (Faster):
```ini
[Settings]
UPLOAD_RESUME = False
```

**Skip Profile Update:**
```ini
UPDATE_PROFILE = False
```

**Run Without Browser** (Headless):
```ini
HEADLESS = True
```

### Adjust Logging

**More Details:**
```ini
[Logging]
LOG_LEVEL = DEBUG
```

**Less Details:**
```ini
LOG_LEVEL = WARNING
```

## 🛑 Managing the Scheduler

### Stop Gracefully
In the scheduler window:
```
Press Ctrl+C
```

The scheduler will:
- Finish current run if in progress
- Save progress data
- Close cleanly

### Stop Forcefully
```powershell
taskkill /IM python.exe /F
```

### Restart
```powershell
run_scheduler.bat
```

## 🔐 Security & Privacy

### Your Data is Safe

✅ **Stored Locally**
- Credentials: `.secrets/secrets.json` (your computer only)
- Logs: `logs/naukri.log` (your computer only)
- Progress: `logs/progress.json` (your computer only)

✅ **Not in GitHub**
- Protected by `.gitignore`
- Only code and config are on GitHub
- Your secrets are never exposed

✅ **No Cloud Storage**
- Everything stays on your machine
- No third-party services involved
- Full privacy guaranteed

### Important
- ⚠️ Never commit `.secrets/secrets.json`
- ⚠️ Never share progress files
- ⚠️ Keep your machine secure

## 📞 Troubleshooting Guide

### Problem: "ModuleNotFoundError"
**Cause**: Missing Python packages
**Solution**: 
```powershell
pip install -r requirements.txt
```

### Problem: "Naukri login failed"
**Cause**: Wrong credentials or account issue
**Solution**:
```powershell
python setup.py  # Reconfigure credentials
run_once.bat     # Test again
```

### Problem: Scheduler won't start
**Cause**: Python not configured
**Solution**:
```powershell
python --version  # Check if Python works
python setup.py   # Reconfigure everything
```

### Problem: Progress dashboard shows no runs
**Cause**: First run hasn't completed yet
**Solution**: Wait for first run to complete (takes 3-5 minutes)

### Problem: Chrome/Browser error
**Cause**: Selenium can't find Chrome
**Solution**:
- Ensure Chrome is installed
- Try enabling headless mode in config.ini

### Problem: Network timeout errors
**Cause**: Internet connection issues
**Solution**: Check internet connection, try run_once.bat again

## 📚 File Reference

| File | Purpose |
|------|---------|
| `run_scheduler.bat` | Start the automated scheduler |
| `run_once.bat` | Run the script once |
| `view_progress.bat` | View progress dashboard |
| `python setup.py` | Configure credentials |
| `python verify_setup.py` | Verify everything is set up |
| `config/config.ini` | Edit settings and frequency |
| `.secrets/secrets.json` | Your credentials (never share!) |
| `logs/naukri.log` | Execution log file |
| `logs/progress.json` | Progress statistics |

## 📖 Documentation Files

| File | Content |
|------|---------|
| `README.md` | Main documentation |
| `QUICK_START.md` | 5-minute setup |
| `SCHEDULER_GUIDE.md` | Scheduling details |
| `SCHEDULING_SETUP.md` | Complete setup guide |
| `PROJECT_SUMMARY.md` | Technical overview |
| `GIT_SETUP.md` | GitHub integration |

## ✨ Pro Tips

### Tip 1: Headless Mode
For faster, quieter operation:
```ini
HEADLESS = True
```

### Tip 2: Check Logs in Real-Time
```powershell
Get-Content logs\naukri.log -Wait  # Live log stream
```

### Tip 3: Backup Your Resume Path
If you update your resume file path:
```powershell
python setup.py  # Just update that field
```

### Tip 4: Monitor Success Rate
Aim for 95%+ success rate. If it's dropping:
1. Check internet connection
2. Check if Naukri changed their page layout
3. Review `logs/naukri.log` for errors

## 🎯 Next Steps

1. ✅ Run `python setup.py` - Configure credentials
2. ✅ Run `run_once.bat` - Test once
3. ✅ Run `run_scheduler.bat` - Start recurring
4. ✅ Run `view_progress.bat` - Check status
5. ✅ Let it run 24/7 - Your profile stays fresh!

## 📊 Expected Results (Weekly)

After one week with 1.5-hour frequency:

- **Runs**: ~112 executions (7 days × 16 per day)
- **Successful**: ~107 (95% success rate)
- **Failed**: ~5 (retry/failures)
- **Total Duration**: ~2-3 hours of actual script running
- **Profile Updates**: Your headline rotates through 10 variations
- **Recruiter Visibility**: Significantly improved due to consistent updates

## 💬 Support

### Check Everything
```powershell
python verify_setup.py
```

### View Recent Activity
```powershell
Get-Content logs\naukri.log -Tail 50
```

### Reset Everything
```powershell
python setup.py
run_once.bat
run_scheduler.bat
```

---

**Your Naukri automation is ready! Happy recruiting! 🚀**

Let your profile work for you while you focus on interviews!
