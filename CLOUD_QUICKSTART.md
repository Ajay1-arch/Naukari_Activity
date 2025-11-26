# Cloud Automation Setup - Quick Start

## 🎯 What You'll Do (3 Steps)

### Step 1: Add 4 Secrets to GitHub
Go to: **https://github.com/Ajay1-arch/Naukari_Activity/settings/secrets/actions**

Click **"New repository secret"** and add:

```
NAUKRI_EMAIL = your_email@gmail.com
NAUKRI_PASSWORD = your_password
NAUKRI_MOBILE = your_mobile_number
RESUME_PATH = /tmp/resume.pdf
```

### Step 2: Upload Your Resume (Optional)
If you want to use your actual resume:
1. Go to your repository main page
2. Click **"Add file" → "Upload files"**
3. Upload your `resume.pdf`
4. Update `RESUME_PATH` secret to: `/home/runner/work/Naukari_Activity/Naukari_Activity/resume.pdf`

### Step 3: Enable the Cloud Scheduler
1. Go to: **https://github.com/Ajay1-arch/Naukari_Activity/actions**
2. Select: **"Naukri Automation - Cloud Scheduler"**
3. Click: **"Run workflow" → "Run workflow"**
4. Watch it execute in real-time!

## ✅ That's It!

The automation will now run automatically **every 2 hours** on GitHub's cloud servers:
- ✅ No local computer needed
- ✅ No screen overlay
- ✅ 24/7 execution
- ✅ Completely free (uses only ~360 of 2000 free monthly minutes)
- ✅ Secure (credentials encrypted in GitHub)

## 📊 Monitor Progress

1. Go to **Actions** tab
2. Click on any workflow run
3. View logs and execution details
4. Download artifacts with full logs

## 🛠️ Advanced Options

See `CLOUD_SETUP.md` for:
- How to change the schedule (run more/less frequently)
- How to monitor logs and progress
- Troubleshooting tips
- Best practices

---

**Your Naukri automation is now running in the cloud! 🚀**
