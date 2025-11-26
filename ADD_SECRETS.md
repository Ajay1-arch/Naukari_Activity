# Adding GitHub Secrets - Complete Guide

## 🔐 Why Secrets Matter

GitHub Secrets store sensitive credentials (email, password, mobile) securely:
- ✅ Encrypted at rest
- ✅ Never visible in logs
- ✅ Only used in Actions
- ✅ Automatically deleted after each run

## Method 1: Automatic (Easiest - Recommended)

### Install GitHub CLI

1. **Download GitHub CLI**
   - Go to: https://cli.github.com/
   - Download for Windows
   - Run the installer and follow steps

2. **Authenticate GitHub CLI**
   ```powershell
   gh auth login
   ```
   - Choose "HTTPS"
   - Choose "Y" for git credential manager
   - Paste token when prompted (or generate one)

3. **Run Secret Setup Script**
   ```powershell
   cd c:\Users\AJAY\Downloads\naukri-automation
   python add_github_secrets.py
   ```
   
   The script will:
   - Read your local `.secrets/secrets.json`
   - Add 4 secrets to GitHub automatically
   - Show confirmation for each

## Method 2: Manual (Through GitHub Website)

### Step 1: Go to Settings
1. Go to: **https://github.com/Ajay1-arch/Naukari_Activity**
2. Click: **Settings** (top right)
3. Left sidebar: **Secrets and variables** → **Actions**

### Step 2: Add 4 Secrets

For each secret below, click **"New repository secret"**:

#### Secret 1: NAUKRI_EMAIL
- **Name**: `NAUKRI_EMAIL`
- **Value**: Your Naukri email (e.g., `Ajaybadugu1999@gmail.com`)
- Click **"Add secret"**

#### Secret 2: NAUKRI_PASSWORD
- **Name**: `NAUKRI_PASSWORD`
- **Value**: Your Naukri password (e.g., `2529@Ajay`)
- Click **"Add secret"**

#### Secret 3: NAUKRI_MOBILE
- **Name**: `NAUKRI_MOBILE`
- **Value**: Your mobile number (e.g., `9959811354`)
- Click **"Add secret"**

#### Secret 4: RESUME_PATH
- **Name**: `RESUME_PATH`
- **Value**: `/tmp/resume.pdf` (for cloud)
- Click **"Add secret"**

### Step 3: Verify
You should see 4 secrets listed:
```
✓ NAUKRI_EMAIL
✓ NAUKRI_PASSWORD
✓ NAUKRI_MOBILE
✓ RESUME_PATH
```

## Method 3: Using GitHub CLI Directly

If you prefer command line after installing GitHub CLI:

```powershell
# Authenticate
gh auth login

# Add secrets
gh secret set NAUKRI_EMAIL -b "Ajaybadugu1999@gmail.com" -R Ajay1-arch/Naukari_Activity
gh secret set NAUKRI_PASSWORD -b "2529@Ajay" -R Ajay1-arch/Naukari_Activity
gh secret set NAUKRI_MOBILE -b "9959811354" -R Ajay1-arch/Naukari_Activity
gh secret set RESUME_PATH -b "/tmp/resume.pdf" -R Ajay1-arch/Naukari_Activity
```

## ✅ Verify Secrets Were Added

After adding all 4 secrets:

1. Go to: **https://github.com/Ajay1-arch/Naukari_Activity/settings/secrets/actions**
2. You should see 4 secrets listed (values are hidden for security)

## 🚀 Next: Test Cloud Execution

Once secrets are added:

1. Go to: **https://github.com/Ajay1-arch/Naukari_Activity/actions**
2. Select: **"Naukri Automation - Cloud Scheduler"**
3. Click: **"Run workflow" → "Run workflow"**
4. Watch execution (2-3 minutes)

## 🔒 Security Notes

✅ **Safe to use**:
- Secrets are encrypted
- Never appear in logs
- Protected by GitHub

❌ **Never do this**:
- Don't hardcode credentials in code
- Don't commit `.secrets/secrets.json` to git
- Don't share screenshots of secrets

## 🛠️ Troubleshooting

### Problem: GitHub CLI not working
**Solution**: 
1. Download from: https://cli.github.com/
2. Restart PowerShell after install
3. Run `gh auth login` to authenticate

### Problem: "Not authenticated" error
**Solution**:
1. Run: `gh auth login`
2. Follow the prompts
3. Try again

### Problem: Can't find secrets in Actions
**Solution**:
1. Verify secrets were added in Settings
2. Check that you're in the correct repository
3. Try refreshing the page

### Problem: Actions fails with "secret not found"
**Solution**:
1. Check secret names match exactly:
   - `NAUKRI_EMAIL` (not `email`)
   - `NAUKRI_PASSWORD` (not `password`)
   - `NAUKRI_MOBILE` (not `mobile`)
   - `RESUME_PATH` (not `path`)
2. Re-add any missing secrets

## 📊 What's Next?

After adding secrets:

✅ Secrets stored safely
✅ GitHub Actions can access them
✅ Cloud execution ready
✅ Naukri automation runs every 2 hours

**All automated! No more manual updates!** 🎉

---

**Choose your method above and follow the steps!**
