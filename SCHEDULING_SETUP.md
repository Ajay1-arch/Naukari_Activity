# Naukri Automation - Scheduling & Progress Tracking Setup

## ✅ What's Been Configured

Your Naukri automation is now fully set up with:

### ⏱️ Scheduling
- **Frequency**: 1.5 hours (90 minutes)
- **Variance**: ±15 minutes (random between 75-105 minutes)
- **Type**: Random timing (avoids detection patterns)
- **Configuration File**: `config/config.ini`

### 📊 Progress Tracking
- **Real-time Statistics**: Success rates, run counts, timing
- **Historical Data**: Complete log of every execution
- **Performance Metrics**: Average/min/max run duration
- **Dashboard**: Visual progress view

### 📁 Files & Directories
```
naukri-automation/
├── src/
│   ├── scheduler.py          # Main scheduler with progress tracking
│   ├── naukri_main.py        # Naukri automation script
│   └── config_loader.py      # Configuration management
├── config/
│   └── config.ini            # Scheduling and settings
├── logs/
│   ├── naukri.log            # Execution logs
│   └── progress.json         # Progress statistics
├── .secrets/
│   └── secrets.json          # Your credentials (not in Git)
├── run_scheduler.bat         # Start the scheduler
├── view_progress.bat         # View progress dashboard
├── run_once.bat              # Run once (no scheduling)
├── SCHEDULER_GUIDE.md        # Detailed scheduling guide
└── README.md                 # Main documentation
```

## 🚀 Quick Start (3 Steps)

### Step 1: Configure Your Credentials
```powershell
cd c:\Users\AJAY\Downloads\naukri-automation
python setup.py
```

You'll be prompted for:
- Naukri email
- Naukri password
- Mobile number
- Resume file path

This creates `.secrets/secrets.json` (securely stored, never pushed to Git).

### Step 2: Test Once
```powershell
run_once.bat
```

This runs the automation once to verify everything works.

### Step 3: Start the Scheduler
```powershell
run_scheduler.bat
```

The scheduler will:
- Run immediately
- Wait 75-105 minutes
- Run again automatically
- Continue forever until you stop it
- Track all progress

## 📊 Monitoring Progress

### View Live Dashboard
At any time, in a new terminal:
```powershell
view_progress.bat
```

Shows:
- Total runs executed
- Success rate
- Recent run history
- Performance statistics

### Check Logs
Real-time execution log:
```powershell
type logs\naukri.log | tail -50
```

Progress statistics:
```powershell
type logs\progress.json
```

## ⚙️ Scheduling Details

### Configuration (config/config.ini)
```ini
[Scheduling]
# 1.5 hours = 5400 seconds
# With ±15 min variance = 4500-6300 seconds (75-105 minutes)
RANDOM_DELAY_MIN = 4500    # 75 minutes
RANDOM_DELAY_MAX = 6300    # 105 minutes
SCHEDULE_INTERVAL_HOURS = 1.5
USE_RANDOM_TIMES = True    # Enable variance
TRACK_PROGRESS = True
PROGRESS_FILE = logs/progress.json
```

### How It Works
1. **Immediate First Run** - Script executes right away
2. **Random Delay** - Waits between 75-105 minutes
3. **Scheduled Run** - Executes again
4. **Progress Logged** - Records success/failure/timing
5. **Next Cycle** - Repeats from step 2

This randomness looks natural to Naukri and avoids detection.

## 📈 Expected Progress Output

### First Run
```
[Run #1] Starting Naukri automation script...
Logging in to Naukri...
Uploading resume...
Updating profile headline...
[Run #1] Script completed successfully in 47.3 seconds
Next run scheduled for: 2025-11-26 14:15:30 (88.5 minutes from now)
```

### Progress Dashboard (After Multiple Runs)
```
SCHEDULER PROGRESS SUMMARY
============================================================
Total Runs:           12
Successful:           11 ✅
Failed:               1  ❌
Success Rate:         91.7%
Last Run Status:      SUCCESS
Scheduler Started:    2025-11-26 12:00:00

RECENT RUNS (Last 12)
─────────────────────────────────────────────────────
Run # │ Time               │ Status    │ Duration
  1   │ 2025-11-26 12:00   │ ✅ SUCCESS│ 47.3s
  2   │ 2025-11-26 14:15   │ ✅ SUCCESS│ 48.1s
  3   │ 2025-11-26 16:42   │ ❌ FAILED │ 12.5s
  ... (9 more runs)
─────────────────────────────────────────────────────

DETAILED STATISTICS
Average Duration:     47.5 seconds
Min Duration:         12.5 seconds
Max Duration:         52.8 seconds
Total Run Time:       570 seconds (0.16 hours)
```

## 🔧 Customization Options

### Change Frequency to 2 Hours
Edit `config/config.ini`:
```ini
RANDOM_DELAY_MIN = 6300    # 105 minutes
RANDOM_DELAY_MAX = 7500    # 125 minutes
SCHEDULE_INTERVAL_HOURS = 2.0
```

### Change Frequency to 1 Hour
Edit `config/config.ini`:
```ini
RANDOM_DELAY_MIN = 3300    # 55 minutes
RANDOM_DELAY_MAX = 3900    # 65 minutes
SCHEDULE_INTERVAL_HOURS = 1.0
```

### Disable Resume Upload (Faster Runs)
Edit `config/config.ini`:
```ini
[Settings]
UPLOAD_RESUME = False
```

### Run Without Browser Window (Headless Mode)
Edit `config/config.ini`:
```ini
[Settings]
HEADLESS = True
```

### Change Log Level to Debug
Edit `config/config.ini`:
```ini
[Logging]
LOG_LEVEL = DEBUG  # More verbose output
```

## 🛑 Stopping the Scheduler

### Method 1: Keyboard Interrupt (Recommended)
In the scheduler window:
```
Press Ctrl+C
```

### Method 2: PowerShell
```powershell
taskkill /IM python.exe /F
```

### Method 3: Task Manager
1. Press `Ctrl+Shift+Esc`
2. Find `python.exe`
3. Click "End Task"

## 📝 Understanding Progress.json

Located at: `logs/progress.json`

### Structure
```json
{
  "scheduler_started": "2025-11-26T12:00:00.000000",
  "total_runs": 3,
  "successful_runs": 3,
  "failed_runs": 0,
  "last_run": "2025-11-26T16:42:15.000000",
  "last_run_status": "SUCCESS",
  "runs": [
    {
      "run_number": 1,
      "timestamp": "2025-11-26T12:00:15.000000",
      "success": true,
      "duration_seconds": 47.3,
      "error": null
    },
    {
      "run_number": 2,
      "timestamp": "2025-11-26T14:15:30.000000",
      "success": true,
      "duration_seconds": 48.1,
      "error": null
    }
  ]
}
```

### Key Fields
- `total_runs` - Total executions
- `successful_runs` - Successful executions
- `failed_runs` - Failed executions
- `runs` - Array of all run details
- `duration_seconds` - How long each run took
- `error` - Error message if failed

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Scheduler won't start** | Run `python setup.py` to configure credentials |
| **Script fails on first run** | Check logs: `type logs\naukri.log` |
| **Progress not updating** | Verify `logs/` directory permissions |
| **Scheduler runs too fast** | Check `RANDOM_DELAY_MIN/MAX` in config.ini |
| **Dashboard shows no data** | Wait for first run to complete, then run `view_progress.bat` |
| **Can't stop scheduler** | Use `Ctrl+C`, or kill process in Task Manager |

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation with all features |
| `SCHEDULER_GUIDE.md` | Detailed scheduling configuration guide |
| `QUICK_START.md` | 5-minute setup guide |
| `PROJECT_SUMMARY.md` | Technical project overview |
| `GIT_SETUP.md` | GitHub integration guide |
| `FILE_INDEX.md` | Complete file reference |

## 🔒 Security & Privacy

✅ **What's Secure:**
- Credentials in `.secrets/secrets.json` (not in Git)
- Progress file contains no sensitive data
- Logs contain no passwords
- All data stays on your computer
- Project is private (only you can access)

⚠️ **Important:**
- Never commit `.secrets/secrets.json`
- Never share progress files publicly
- Check that `.secrets/` is in `.gitignore`

## 💾 Git Integration

All files are version controlled on GitHub:
```
Repository: https://github.com/Ajay1-arch/Naukari_Activity
Branch: main
```

### What's on GitHub
- ✅ All source code
- ✅ Configuration templates
- ✅ Documentation
- ✅ Setup scripts

### What's NOT on GitHub
- ❌ `.secrets/secrets.json` (your credentials)
- ❌ `logs/naukri.log` (execution logs)
- ❌ `logs/progress.json` (progress data)

Protected by `.gitignore` - safe from accidental commits.

## 🎯 Next Actions

1. **Run credentials setup**:
   ```powershell
   python setup.py
   ```

2. **Test once to verify**:
   ```powershell
   run_once.bat
   ```

3. **Start the scheduler**:
   ```powershell
   run_scheduler.bat
   ```

4. **Monitor progress** (in a new terminal):
   ```powershell
   view_progress.bat
   ```

5. **Let it run** - The scheduler handles everything!

## 📞 Support & Questions

### Check Everything Works
```powershell
python verify_setup.py
```

### View Recent Logs
```powershell
type logs\naukri.log | tail -50
```

### Reset & Start Over
```powershell
python setup.py
run_once.bat
run_scheduler.bat
```

---

**Your Naukri automation is ready to run 24/7! 🚀**

Keep your profile visible to recruiters with automated updates every 1.5 hours.
