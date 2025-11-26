# Naukri Automation Script

Automatically update your Naukri profile daily - upload resume, update profile information, and rotate professional headlines to attract recruiters!

## Features

- ✅ **Automatic Login** - Securely logs into Naukri
- ✅ **Resume Upload** - Daily resume upload with timestamp verification
- ✅ **Profile Updates** - Update mobile number and other profile info
- ✅ **Headline Rotation** - 10 different professional headlines that rotate
- ✅ **PDF Modification** - Optional: Add hidden text to resume (anti-scraping measure)
- ✅ **Scheduled Execution** - Run hourly or at random intervals
- ✅ **Secure Configuration** - Secrets stored separately, not in git
- ✅ **Comprehensive Logging** - All actions logged for debugging

## Project Structure

```
naukri-automation/
├── .secrets/                 # Secrets folder (in .gitignore)
│   ├── secrets.json         # Your credentials (DO NOT COMMIT)
│   └── secrets.template.json # Template for secrets
├── config/
│   └── config.ini           # Configuration file
├── src/
│   ├── config_loader.py     # Load secrets and config
│   ├── scheduler.py         # Scheduler for periodic execution
│   └── naukri_main.py       # Main automation script
├── logs/                     # Log files
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
├── setup.py               # Setup script
├── run_once.bat           # Run script once
├── run_scheduler.bat      # Run scheduler continuously
└── README.md              # This file
```

## Installation

### 1. Clone/Download the Repository

```bash
git clone <your-repo-url> naukri-automation
cd naukri-automation
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Secrets and Configuration

```bash
python setup.py
```

This will:
- Ask for your Naukri credentials
- Ask for your resume file paths
- Create `secrets.json` with your information
- Save configuration to `config/config.ini`

**Important:** The `.secrets/` folder is in `.gitignore` - your secrets will NEVER be committed to git!

## Usage

### Option 1: Run Once Manually

```bash
python src/naukri_main.py
```

Or use the batch file:
```bash
run_once.bat
```

### Option 2: Run Scheduler (Continuous Execution)

```bash
python src/scheduler.py
```

Or use the batch file:
```bash
run_scheduler.bat
```

The scheduler will:
- Run the script immediately
- Then repeat at configured intervals (default: every hour)
- Can use random times for less predictable behavior

### Option 3: Schedule with Windows Task Scheduler (Best for Automation)

#### Using Task Scheduler GUI:

1. Open **Task Scheduler** (search in Windows)
2. Click **Create Basic Task**
3. **Name**: "Naukri Automation"
4. **Trigger**: Daily at specific time (or hourly, or custom)
5. **Action**: 
   - Program: `C:\path\to\python\python.exe`
   - Arguments: `src\naukri_main.py`
   - Start in: `C:\path\to\naukri-automation\`

#### Using PowerShell (Automated):

```powershell
# Create task to run every hour
$trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 1) -At (Get-Date) -Once
$action = New-ScheduledTaskAction -Execute "C:\path\to\python\python.exe" -Argument "src\naukri_main.py" -WorkingDirectory "C:\path\to\naukri-automation"
Register-ScheduledTask -TaskName "Naukri Automation" -Trigger $trigger -Action $action -RunLevel Highest
```

## Configuration

Edit `config/config.ini` to customize:

```ini
[URLs]
NAUKRI_LOGIN_URL = https://login.naukri.com/nLogin/Login.php
NAUKRI_PROFILE_URL = https://www.naukri.com/mnjuser/profile?id=&altresid

[Settings]
UPDATE_PDF = False              # Add hidden text to resume
HEADLESS = False                # Run Chrome in headless mode
UPLOAD_RESUME = True            # Enable resume upload
UPDATE_PROFILE = True           # Enable profile updates

[Logging]
LOG_LEVEL = INFO
LOG_FILE = logs/naukri.log
MAX_LOG_SIZE = 10485760        # 10MB

[Scheduling]
RANDOM_DELAY_MIN = 300          # Min delay (seconds)
RANDOM_DELAY_MAX = 1800         # Max delay (seconds)
SCHEDULE_INTERVAL_HOURS = 1     # Run every N hours
USE_RANDOM_TIMES = True         # Use random times
```

## Available Headlines

The script rotates through 10 professional headlines:

1. Data Engineer | BigQuery | Cloud Composer | Python | SAP BODS
2. GCP Certified Senior Data Engineer | Cloud Analytics | AI/ML
3. Data Pipeline Expert | Airflow | Talend | Cloud Architecture
4. BigQuery Specialist | ETL/ELT | Data Lakehouse | Cloud Solutions
5. Cloud Data Engineer | Tableau | Power BI | Analytics | GCP/Azure
6. Data Engineering Lead | SQL | PySpark | Enterprise Solutions
7. Analytics Engineer | Cloud-Native | Data Quality | Business Intelligence
8. Senior Data Engineer | SAP Migration | Financial Analytics | Healthcare
9. Data Architect | Cloud Platforms | 3+ YRS | Team Lead | AI-Assisted Dev
10. BigQuery Expert | Python | SQL | AI-Driven Analytics | 400+ Users Supported

Each run rotates to a different headline (when the feature is fully enabled).

## Troubleshooting

### Script says "Wrong Site"
- Check the login URL in `config/config.ini`
- Naukri may have updated their site structure

### Credentials not working
- Verify email/password in `.secrets/secrets.json`
- Check if 2FA is enabled on your account
- Run `python setup.py` to reconfigure

### Resume not uploading
- Verify file path in `.secrets/secrets.json`
- Check file permissions
- Ensure resume file exists

### Chrome not launching
- Ensure Chrome is installed
- Check if chromedriver is in PATH

## Log Files

Logs are saved to `logs/naukri.log`

View recent logs:
```bash
# Windows
type logs\naukri.log | findstr /R ".*" | tail -50

# Linux/Mac
tail -50 logs/naukri.log
```

## Security Notes

- ✅ Secrets are stored in `.secrets/secrets.json` (in `.gitignore`)
- ✅ Credentials are NOT hardcoded in scripts
- ✅ Configuration is separated from secrets
- ✅ Safe to push to GitHub (secrets won't leak)

### Best Practices

1. **Never commit `.secrets/` folder**
   - It's already in `.gitignore`
   - Double-check before pushing

2. **Keep your credentials safe**
   - Don't share `secrets.json`
   - Use strong passwords

3. **Monitor execution logs**
   - Check `logs/naukri.log` regularly
   - Alert on failures

## Git Push Example

```bash
# Initialize git repo
git init
git add .
git commit -m "Initial commit: Naukri automation setup"
git remote add origin <your-github-url>
git push -u origin main

# Your secrets will NOT be included (they're in .gitignore)
```

## API & Customization

### Add Custom Headlines

Edit `src/naukri_main.py`:

```python
PROFILE_HEADLINES = [
    "Your Custom Headline 1",
    "Your Custom Headline 2",
    # Add more...
]
```

### Modify Update Frequency

In `config/config.ini`:

```ini
[Scheduling]
SCHEDULE_INTERVAL_HOURS = 2     # Run every 2 hours
USE_RANDOM_TIMES = False        # Use fixed intervals
```

Or:

```ini
[Scheduling]
RANDOM_DELAY_MIN = 300          # 5 minutes
RANDOM_DELAY_MAX = 3600         # 60 minutes
USE_RANDOM_TIMES = True         # Random timing
```

## Known Limitations

- 🔄 Headline rotation requires finding the correct field selector
- 🔐 2FA support not yet implemented
- 📱 Mobile validation requires manual verification sometimes

## Future Enhancements

- [ ] Headline field auto-detection
- [ ] 2FA support
- [ ] Email notifications on success/failure
- [ ] Web dashboard for monitoring
- [ ] Multi-account support

## Support

If you encounter issues:

1. Check logs: `logs/naukri.log`
2. Run with debug mode enabled
3. Verify credentials in `.secrets/secrets.json`
4. Try running manually: `python src/naukri_main.py`

## License

MIT License - Feel free to use and modify!

## Disclaimer

This tool is for personal use only. Use responsibly and comply with Naukri's Terms of Service.

---

**Happy Job Hunting! 🚀**
