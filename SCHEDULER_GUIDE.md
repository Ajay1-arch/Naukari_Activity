# Scheduler Setup & Progress Tracking Guide

## ✨ What's New

Your Naukri automation scheduler is now configured with:

- **⏱️ Frequency**: 1.5 hours (90 minutes) between runs
- **🎲 Variance**: ±15 minutes (random timing between 75-105 minutes)
- **📊 Progress Tracking**: Real-time statistics in JSON format
- **📈 Dashboard**: Beautiful progress visualization
- **📝 Detailed Logs**: Complete execution history with timestamps and durations

## 🚀 Getting Started

### Option 1: Simple Batch File (Recommended for Windows)

```batch
run_scheduler.bat
```

This will:
- Start the scheduler with visual feedback
- Run the first script immediately
- Schedule subsequent runs at 1.5-hour intervals with random variance
- Save all progress to `logs/progress.json`

### Option 2: PowerShell (Advanced)

```powershell
powershell -ExecutionPolicy Bypass -File start-scheduler-advanced.ps1
```

This provides:
- Pre-flight checks (credentials verification)
- Detailed startup information
- Helpful tips for monitoring

## 📊 Monitoring Progress

### View Dashboard

To see your scheduler's progress at any time:

```batch
view_progress.bat
```

Or directly:

```bash
python view_progress.py
```

The dashboard shows:
- **Total Runs**: Number of times the script has executed
- **Successful**: How many ran without errors
- **Failed**: How many encountered issues
- **Success Rate**: Percentage of successful executions
- **Recent Runs**: Last 15 executions with timestamps, status, and duration
- **Statistics**: Average, min, max run duration

### Example Dashboard Output

```
╔══════════════════════════════════════════════════════════╗
║     NAUKRI AUTOMATION - SCHEDULER DASHBOARD              ║
╚══════════════════════════════════════════════════════════╝

============================================================
SCHEDULER PROGRESS SUMMARY
============================================================
Total Runs:           12
Successful:           11
Failed:               1
Success Rate:         91.7%
Last Run Status:      SUCCESS
Last Run Time:        2025-11-26T15:30:45
Scheduler Started:    2025-11-26T12:00:00
============================================================

RECENT RUNS (Last 12)
────────────────────────────────────────────────────────────
Run # │ Timestamp           │ Status      │ Duration │ Error
    1 │ 2025-11-26 12:00:15 │ ✓ SUCCESS   │ 45.2s    │ -
    2 │ 2025-11-26 13:52:30 │ ✗ FAILED    │ 12.1s    │ TimeoutError
    3 │ 2025-11-26 15:30:45 │ ✓ SUCCESS   │ 48.5s    │ -
────────────────────────────────────────────────────────────

DETAILED STATISTICS
────────────────────────────────────────────────────────────
Average Run Duration: 45.3 seconds
Minimum Duration:     12.1 seconds
Maximum Duration:     52.8 seconds
Total Run Time:       543.6 seconds (0.15 hours)
────────────────────────────────────────────────────────────
```

## 📁 Log Files & Data

### Progress File
**Location**: `logs/progress.json`

```json
{
  "scheduler_started": "2025-11-26T12:00:00",
  "total_runs": 12,
  "successful_runs": 11,
  "failed_runs": 1,
  "last_run": "2025-11-26T15:30:45",
  "last_run_status": "SUCCESS",
  "runs": [
    {
      "run_number": 1,
      "timestamp": "2025-11-26T12:00:15",
      "success": true,
      "duration_seconds": 45.2,
      "error": null
    },
    ...
  ]
}
```

### Execution Logs
**Location**: `logs/naukri.log`

Contains detailed execution information:
- Script startup and shutdown
- Resume upload confirmation
- Profile headline updates
- Browser actions and clicks
- Errors and exceptions with full tracebacks
- Run numbers and timing information

Example log entry:
```
2025-11-26 12:00:15,123 - INFO - [Run #1] Starting Naukri automation script...
2025-11-26 12:00:15,456 - INFO - Initializing SeleniumBase webdriver...
2025-11-26 12:00:32,789 - INFO - Successfully logged in to Naukri
2025-11-26 12:00:45,123 - INFO - Resume uploaded successfully
2025-11-26 12:00:50,456 - INFO - [Run #1] Script completed successfully in 45.2 seconds
```

## ⚙️ Scheduling Configuration

All settings are in `config/config.ini`:

```ini
[Scheduling]
# 1.5 hour frequency with ±15 minute variance
RANDOM_DELAY_MIN = 4500    # 75 minutes (in seconds)
RANDOM_DELAY_MAX = 6300    # 105 minutes (in seconds)
SCHEDULE_INTERVAL_HOURS = 1.5
USE_RANDOM_TIMES = True    # Enable random variance
TRACK_PROGRESS = True
PROGRESS_FILE = logs/progress.json
```

### How It Works

1. **First Run**: Script runs immediately
2. **Random Delay**: Waits between 75-105 minutes (1h15m - 1h45m)
3. **Scheduled Run**: Executes the Naukri update
4. **Progress Saved**: Adds run data to progress.json
5. **Next Cycle**: Repeats from step 2

The variance ensures you're not always updating at the exact same time, which looks more natural to Naukri's systems.

## 🛑 Stopping the Scheduler

### Method 1: From the Window
Press **Ctrl+C** in the scheduler window

### Method 2: From Command Line
```powershell
taskkill /IM python.exe /F
```

### Method 3: Task Manager
1. Open Task Manager (Ctrl+Shift+Esc)
2. Find python.exe
3. Click "End Task"

## 🔄 Modifying Schedule

To change the frequency (e.g., 2 hours instead of 1.5):

1. Edit `config/config.ini`
2. Update:
   ```ini
   # For 2 hours with ±15 min variance:
   RANDOM_DELAY_MIN = 6300    # 105 minutes
   RANDOM_DELAY_MAX = 7500    # 125 minutes
   SCHEDULE_INTERVAL_HOURS = 2
   ```
3. Restart the scheduler

## 📈 Performance Tips

1. **Monitor Success Rate**: Check dashboard regularly
   - Aim for 95%+ success rate
   - Investigate failed runs in logs/naukri.log

2. **Check Run Duration**: 
   - Normal: 40-60 seconds
   - If consistently > 90 seconds, check your internet connection
   - If < 20 seconds, script may be finishing early (check logs)

3. **Resume Upload**:
   - Only enable if you update your resume frequently
   - Disable to speed up runs: set `UPLOAD_RESUME = False` in config.ini

4. **Headless Mode**:
   - Set `HEADLESS = True` to run without opening browser
   - Faster and uses less system resources

## 🐛 Troubleshooting

### Scheduler Won't Start
**Problem**: "ModuleNotFoundError" when running scheduler
**Solution**: Install dependencies
```powershell
pip install -r requirements.txt
```

### Progress File Not Updating
**Problem**: `logs/progress.json` is empty or not created
**Solution**: 
- Check if script ran: look for entries in `logs/naukri.log`
- Verify directory permissions on the logs folder
- Check that `TRACK_PROGRESS = True` in config.ini

### Dashboard Shows No Runs
**Problem**: `view_progress.py` says "No progress data found"
**Solution**:
- Wait for first run to complete
- Check scheduler is running: `tasklist | find "python"`
- Verify `logs/` directory exists

### Scheduler Runs Too Fast or Too Slow
**Problem**: Runs are happening at wrong intervals
**Solution**:
1. Check `USE_RANDOM_TIMES` setting
2. Verify RANDOM_DELAY_MIN and RANDOM_DELAY_MAX
3. Look at actual intervals in logs/naukri.log
4. Restart scheduler after config changes

## 📚 Files in This Update

| File | Purpose |
|------|---------|
| `config/config.ini` | Updated with 1.5-hour scheduling config |
| `src/scheduler.py` | Enhanced with progress tracking |
| `view_progress.py` | Dashboard for viewing statistics |
| `view_progress.bat` | Easy dashboard launcher |
| `start-scheduler-advanced.ps1` | Advanced startup script |
| `run_scheduler.bat` | Updated with better feedback |
| `requirements.txt` | Added tabulate library |

## 💡 Example Usage Scenarios

### Scenario 1: Set & Forget
```batch
run_scheduler.bat
```
- Let it run in the background
- Comes back to check progress occasionally
- Perfect for passive visibility boost

### Scenario 2: Active Monitoring
```batch
REM Terminal 1: Start scheduler
run_scheduler.bat

REM Terminal 2: Monitor progress (every 5 minutes)
view_progress.bat
```
- Real-time visibility
- Quick response to failures

### Scenario 3: Custom Schedule
Edit `config/config.ini` for different frequency:
- **Hourly**: RANDOM_DELAY_MIN=3000, MAX=3600
- **2 Hours**: RANDOM_DELAY_MIN=6300, MAX=7500
- **30 Minutes**: RANDOM_DELAY_MIN=1500, MAX=1800

## 🎯 Expected Behavior

### Normal Operation
```
[Run #1] Starting Naukri automation script...
[Run #1] Script completed successfully in 47.3 seconds
Next run scheduled for: 2025-11-26 14:15:30 (88.5 minutes from now)
```

### With Progress
```
╔════════════════════════════════════════╗
║     SCHEDULER PROGRESS SUMMARY        ║
╠════════════════════════════════════════╣
║ Total Runs:      5                    ║
║ Successful:      5                    ║
║ Failed:          0                    ║
║ Success Rate:    100.0%               ║
║ Last Run:        SUCCESS              ║
╚════════════════════════════════════════╝
```

## 🔒 Security Note

- Your credentials are in `.secrets/secrets.json` (NOT committed to Git)
- Progress file is safe - contains no sensitive data
- Logs may contain technical details but no passwords
- Entire project is private - only you have access

---

**Questions?** Check the main `README.md` or look at example log files in `logs/naukri.log` (after first run)
