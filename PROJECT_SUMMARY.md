# Naukri Automation - Project Structure & Setup Complete

## 📁 Project Created at:
`c:/Users/AJAY/Downloads/naukri-automation/`

## 📂 Directory Structure

```
naukri-automation/
├── .secrets/
│   ├── secrets.json              ← YOUR CREDENTIALS (private, in .gitignore)
│   └── secrets.template.json     ← Template for reference
├── config/
│   └── config.ini               ← Configuration settings
├── src/
│   ├── config_loader.py         ← Loads secrets & config
│   ├── scheduler.py             ← Runs script on schedule
│   └── naukri_main.py          ← Main automation script
├── logs/
│   └── naukri.log              ← Execution logs
├── .gitignore                   ← Git ignore rules
├── requirements.txt             ← Python dependencies
├── setup.py                    ← Initial setup script
├── run_once.bat               ← Run script once (Windows)
├── run_scheduler.bat          ← Run scheduler (Windows)
├── README.md                  ← Full documentation
├── QUICK_START.md            ← 5-minute setup guide
└── PROJECT_SUMMARY.md        ← This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```powershell
cd c:\Users\AJAY\Downloads\naukri-automation
pip install -r requirements.txt
```

### 2. Setup (Interactive)
```powershell
python setup.py
```
Answers prompts:
- Naukri email
- Naukri password
- Mobile number
- Resume file paths
- Chrome settings

### 3. Test It
```powershell
python src/naukri_main.py
```

### 4. Schedule It
**Option A: Run Scheduler (Continuous)**
```powershell
python src/scheduler.py
```

**Option B: Windows Task Scheduler (Recommended)**
```powershell
# Create hourly task
schtasks /create /tn "Naukri Automation Hourly" /tr "C:\Users\AJAY\Downloads\naukri-automation\run_once.bat" /sc hourly /mo 1
```

**Option C: Run at Startup**
```powershell
# Create startup task
schtasks /create /tn "Naukri Automation" /tr "C:\Users\AJAY\Downloads\naukri-automation\run_scheduler.bat" /sc onstart /ru system
```

## 🔒 Security

✅ **Secrets Management:**
- Credentials stored in `.secrets/secrets.json`
- File is in `.gitignore` - NEVER committed to git
- Separate from code for safety

✅ **Git Safe:**
- `.secrets/` folder excluded
- `logs/` folder can be excluded
- Safe to push to public repos

## 📋 Configuration

**`config/config.ini`** - Customize behavior:

```ini
[Settings]
UPDATE_PDF = False              # Add hidden chars to resume
HEADLESS = False                # Chrome in headless mode
UPLOAD_RESUME = True            # Enable resume upload
UPDATE_PROFILE = True           # Enable profile updates

[Scheduling]
SCHEDULE_INTERVAL_HOURS = 1     # Run every 1 hour
USE_RANDOM_TIMES = True         # Use random delays
RANDOM_DELAY_MIN = 300          # Min 5 minutes
RANDOM_DELAY_MAX = 1800         # Max 30 minutes
```

## 📊 What the Script Does

Each run:
1. ✅ Logs into Naukri
2. ✅ Views your profile
3. ✅ Updates headline (when field found)
4. ✅ Uploads resume with timestamp
5. ✅ Logs out cleanly
6. ✅ Logs everything to `logs/naukri.log`

## 🎯 Available Headlines (10 Variations)

Script rotates through these daily:

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

## 📝 Files Created

| File | Purpose |
|------|---------|
| **config_loader.py** | Loads secrets & config from JSON/INI files |
| **scheduler.py** | Runs script on schedule (hourly or random) |
| **naukri_main.py** | Main automation logic (refactored from original) |
| **config.ini** | Settings file (not private) |
| **secrets.template.json** | Template showing required fields |
| **secrets.json** | YOUR credentials (in .gitignore) |
| **setup.py** | Interactive setup script |
| **run_once.bat** | Windows batch to run once |
| **run_scheduler.bat** | Windows batch to run scheduler |
| **.gitignore** | Prevents committing secrets |
| **README.md** | Full documentation |
| **QUICK_START.md** | 5-minute setup guide |

## 🔧 Customization Examples

**Change Schedule (Run Every 2 Hours):**
```ini
[Scheduling]
SCHEDULE_INTERVAL_HOURS = 2
USE_RANDOM_TIMES = False
```

**Add Custom Headlines:**
Edit `src/naukri_main.py`:
```python
PROFILE_HEADLINES = [
    "Your Custom Headline 1",
    "Your Custom Headline 2",
]
```

**Run in Headless Mode (No Browser Window):**
```ini
[Settings]
HEADLESS = True
```

## 📊 Logging

All actions logged to `logs/naukri.log`:

```
2025-11-26 14:30:12 : -----Naukri.py Script Run Begin-----
2025-11-26 14:30:13 : Google Chrome Launched!
2025-11-26 14:30:15 : Website Loaded Successfully.
2025-11-26 14:30:20 : Naukri Login Successful
2025-11-26 14:30:25 : Starting Profile Update...
2025-11-26 14:31:00 : Starting Resume Upload...
2025-11-26 14:31:15 : Resume Document Upload Successful
2025-11-26 14:31:16 : Logout Successful
2025-11-26 14:31:16 : -----Naukri.py Script Run Ended-----
```

## 📂 Git Repository Setup

**Initialize Git:**
```bash
cd naukri-automation
git init
git add .
git commit -m "Initial commit: Naukri automation setup"
git remote add origin <your-github-url>
git push -u origin main
```

**Verify Secrets Not Committed:**
```bash
git ls-files | grep -i secret
# Should return nothing
```

## ✅ Checklist

- [x] Project structure created
- [x] Secrets management setup
- [x] Configuration system implemented
- [x] Scheduler created
- [x] Setup script created
- [x] Batch files created
- [x] Documentation written
- [ ] **Next: Run `python setup.py` to configure**
- [ ] **Next: Run `python src/naukri_main.py` to test**
- [ ] **Next: Setup Windows Task Scheduler**
- [ ] **Next: Push to GitHub**

## 🚨 Important Notes

1. **Secrets File**: After running `setup.py`, your credentials are in `.secrets/secrets.json`
   - This file is in `.gitignore`
   - It's safe to push other files to GitHub
   - Never manually add this file to git

2. **Configuration**: You can customize everything in `config/config.ini`
   - This file IS safe to commit
   - Contains no sensitive data

3. **Logs**: Check `logs/naukri.log` if anything fails
   - Shows detailed execution trace
   - Helps troubleshoot issues

4. **Dependencies**: All required packages in `requirements.txt`
   - Install with: `pip install -r requirements.txt`
   - Uses: selenium, pypdf, reportlab

## 🎯 Next Steps

1. **Run Setup:**
   ```powershell
   python setup.py
   ```

2. **Test Manually:**
   ```powershell
   python src/naukri_main.py
   ```

3. **Check Logs:**
   ```powershell
   Get-Content logs/naukri.log -Tail 20
   ```

4. **Schedule Hourly:**
   ```powershell
   python src/scheduler.py
   # OR use Windows Task Scheduler
   ```

5. **Push to GitHub:**
   ```bash
   git push origin main
   ```

## 📞 Support

- See `README.md` for full documentation
- See `QUICK_START.md` for 5-minute setup
- Check `logs/naukri.log` for troubleshooting
- Review `config.ini` for all available options

---

**All set! Your Naukri automation is ready to deploy! 🚀**

For Git security: Your secrets will NEVER be committed.
For automation: Schedule hourly or on startup.
For monitoring: Check logs regularly.
