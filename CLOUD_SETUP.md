# Cloud-Based Execution Setup (GitHub Actions)

## 🚀 Overview

Your Naukri automation now runs **in the cloud for free** using GitHub Actions:

- ✅ **No Local Computer Needed** - Runs on GitHub's servers
- ✅ **24/7 Execution** - Automatic scheduling
- ✅ **Headless Mode** - No screen overlay
- ✅ **Free** - GitHub provides 2000 free Action minutes per month
- ✅ **Secure** - Secrets stored encrypted in GitHub
- ✅ **Logs Tracked** - All execution history saved

## 📋 Setup Instructions (5 Steps)

### Step 1: Add GitHub Secrets
Your credentials need to be added as GitHub Secrets (encrypted):

1. Go to: **https://github.com/Ajay1-arch/Naukari_Activity/settings/secrets/actions**
2. Click **"New repository secret"** and add these 4 secrets:

| Secret Name | Value |
|---|---|
| `NAUKRI_EMAIL` | Your Naukri login email |
| `NAUKRI_PASSWORD` | Your Naukri password |
| `NAUKRI_MOBILE` | Your registered mobile number |
| `RESUME_PATH` | `/tmp/resume.pdf` (see note below) |

**⚠️ Important**: These secrets are encrypted and only used in Actions, never exposed.

### Step 2: Prepare Your Resume
Since GitHub Actions runs in the cloud, you need to upload your resume:

**Option A: Upload Resume File to Repository** (Recommended)
1. Go to your repository: https://github.com/Ajay1-arch/Naukari_Activity
2. Click **"Add file" → "Upload files"**
3. Upload your `resume.pdf` to the root directory
4. Set `RESUME_PATH` secret to: `/home/runner/work/Naukari_Activity/Naukari_Activity/resume.pdf`

**Option B: Use Default Path**
Keep `RESUME_PATH` as: `/tmp/resume.pdf` (will be created/used during execution)

### Step 3: Test the Workflow
1. Go to: **Actions** tab in your repository
2. Select: **"Naukri Automation - Cloud Scheduler"**
3. Click: **"Run workflow" → "Run workflow"**
4. Wait for execution to complete (2-3 minutes)

### Step 4: Monitor Execution
1. Check the workflow run status
2. View logs by clicking on the job
3. Logs are saved as artifacts (downloadable for 7 days)

### Step 5: Verify Success
Once workflow completes:
- ✅ Check the "Logs" section for execution details
- ✅ Check the "Artifacts" section for `naukri-logs.zip`
- ✅ Extract and review `logs/progress.json` for statistics

## ⏱️ Scheduling

### Current Schedule
The workflow runs **every 2 hours automatically**:

```yaml
on:
  schedule:
    - cron: '0 */2 * * *'  # Every 2 hours
```

**Note**: GitHub has a minimum 5-minute interval for Actions, but we're running every 2 hours to:
- Balance execution frequency
- Avoid API rate limits
- Save free monthly minutes

### To Change Schedule

Edit `.github/workflows/naukri-scheduler.yml`:

**Run every 1.5 hours** (Advanced - uses more minutes):
```yaml
- cron: '0 0 * * *'       # Daily (conservative)
- cron: '0 */1 * * *'     # Hourly (uses more minutes)
```

**Run at specific times**:
```yaml
- cron: '0 9,12,18 * * *' # 9 AM, 12 PM, 6 PM (UTC)
```

**Run every week**:
```yaml
- cron: '0 10 * * 1'      # Every Monday at 10 AM UTC
```

Then commit and push the change.

## 💻 How It Works

### Execution Flow

```
1. Trigger: GitHub detects scheduled time or manual trigger
2. Setup: Creates Ubuntu Linux environment
3. Install: Installs Python, pip, dependencies (pypdf, selenium, etc.)
4. Secrets: Loads your credentials from GitHub Secrets
5. Execute: Runs src/naukri_main.py in headless mode
6. Log: Saves logs to logs/naukri.log and logs/progress.json
7. Upload: Saves logs as artifact (visible for 7 days)
8. Cleanup: Removes environment, securely deletes secrets
```

### Key Features

✅ **Secure**: Secrets never exposed in logs
✅ **Isolated**: Fresh environment each run
✅ **Headless**: No browser window
✅ **Logged**: Full execution history preserved
✅ **Automatic**: No manual intervention needed

## 📊 Monitoring

### View Workflow Runs
1. Go to: **https://github.com/Ajay1-arch/Naukari_Activity/actions**
2. Click on any workflow run
3. See execution status and logs

### Download Logs
After execution:
1. Go to the completed workflow run
2. Click **"Artifacts"** section
3. Download `naukri-logs` (ZIP file with all logs)

### Check Progress
Extract the logs and view `progress.json`:
```json
{
  "total_runs": 15,
  "successful_runs": 14,
  "failed_runs": 1,
  "success_rate": 93.3%
}
```

## 🆓 Free Tier Limits

GitHub provides **2000 free minutes per month** for Actions:

| Schedule | Monthly Cost |
|---|---|
| Every 2 hours | ~360 minutes ✅ |
| Every 1.5 hours | ~480 minutes ✅ |
| Every hour | ~720 minutes ✅ |
| Every 30 minutes | ~1440 minutes ✅ |
| Every 15 minutes | ~2880 minutes ❌ (exceeds limit) |

**Current setting (every 2 hours) uses only ~360 minutes = 18% of free allowance**

## 🔧 Troubleshooting

### Problem: Workflow fails with "credentials error"
**Solution**: Check GitHub Secrets are set correctly:
1. Go to Settings → Secrets
2. Verify all 4 secrets are present
3. Re-add if needed

### Problem: "Selenium error" or "Chrome not found"
**Solution**: This should work automatically on GitHub's Ubuntu runners. If not:
1. Check logs for exact error
2. Ensure Chrome/Chromium is installed (it is by default)
3. Try re-running the workflow

### Problem: Resume not uploading
**Solution**: 
1. Ensure resume file is in repository root
2. Update `RESUME_PATH` secret to correct path
3. Or use `/tmp/resume.pdf` (default)

### Problem: "Out of free minutes"
**Solution**: 
1. Reduce frequency (run every 3-4 hours instead)
2. Edit the cron schedule in `.github/workflows/naukri-scheduler.yml`
3. Or use local execution instead

## 🔄 Switching Between Local & Cloud

### Run Locally (Testing)
```powershell
cd c:\Users\AJAY\Downloads\naukri-automation
.\run_scheduler.bat
```

### Run on Cloud (Production)
Just commit to GitHub - Actions runs automatically on schedule!

### Disable Cloud Execution
Go to: **Settings → Actions** → **Disable Actions** (to disable temporarily)

## 📈 Best Practices

1. **Monitor Regularly**: Check Actions tab weekly
2. **Check Logs**: Review execution logs for errors
3. **Keep Secrets Safe**: Never hardcode credentials
4. **Update Resume**: If you change your resume, update in repository
5. **Test Before Deploying**: Run manually first to verify

## 🎯 Complete Workflow

```
Day 1: Setup (this page)
  ↓
Day 2: First Scheduled Run (automatic)
  ↓
Every 2 Hours: Naukri Profile Updated (automatic)
  ↓
Weekly: Check logs and success rate
  ↓
Monthly: Review progress from artifacts
```

## 📞 Support

### Check Execution Status
1. Go to **Actions** tab
2. Click latest workflow run
3. See detailed logs

### Manual Trigger
1. Go to **Actions** tab
2. Select **"Naukri Automation - Cloud Scheduler"**
3. Click **"Run workflow"**

### View All Runs
Click **"All workflows"** to see complete history

## ✨ Advanced: Custom Schedule

Want different timing? Edit the cron schedule:

1. Go to `.github/workflows/naukri-scheduler.yml` in your repository
2. Find the `cron` line
3. Update to your preferred schedule
4. Commit and push

Example schedules:
```yaml
'0 9 * * *'       # Daily at 9 AM
'0 9,17 * * *'    # 9 AM and 5 PM
'0 */4 * * *'     # Every 4 hours
'0 0 * * 0'       # Weekly (Sunday at midnight)
```

---

**Your Naukri automation is now running 24/7 in the cloud! 🚀**

No local computer needed. Profile stays fresh automatically!
