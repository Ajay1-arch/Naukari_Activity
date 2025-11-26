# Git Repository Setup Guide

## Why Git?

Git allows you to:
- ✅ Version control your automation script
- ✅ Store code safely (without credentials)
- ✅ Share on GitHub (publicly safe)
- ✅ Backup your code
- ✅ Track changes over time

## Security First

**Important:** Your secrets are NEVER committed to git!

- `✓ SAFE` to commit: `config/`, `src/`, `requirements.txt`, `README.md`
- `✗ NEVER commit`: `.secrets/secrets.json` (it's in .gitignore)
- `⚠ Be careful with: logs/` (may contain sensitive info)

## Step 1: Initialize Local Git

```bash
cd naukri-automation
git init
```

## Step 2: Verify .gitignore

The `.gitignore` file already excludes sensitive data:

```
.secrets/
logs/
__pycache__/
*.pyc
.env
```

Verify it's working:
```bash
# This should show nothing (secrets not tracked)
git ls-files --others --ignored --exclude-standard
```

## Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. Create new repository: `naukri-automation`
3. **Do NOT initialize with README** (you have one)
4. Copy the HTTPS URL

## Step 4: Add Remote and Push

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/naukri-automation.git

# Rename branch to main (if needed)
git branch -M main

# Stage all files
git add .

# Commit
git commit -m "Initial commit: Naukri automation setup"

# Push to GitHub
git push -u origin main
```

## Step 5: Verify No Secrets

Check GitHub repository online:
- You should see: `config/`, `src/`, `README.md`, etc.
- You should NOT see: `.secrets/` folder content

Verify locally:
```bash
# Should be empty
git status .secrets/
```

## Regular Git Workflow

```bash
# Make changes
nano config/config.ini
# or edit src/naukri_main.py

# Check what changed
git status

# Stage changes
git add .

# Commit with message
git commit -m "Update: Changed schedule to 2 hours"

# Push to GitHub
git push origin main
```

## Collaborating (Optional)

If you want to share with others:

1. Push to GitHub
2. Add collaborators: Settings → Collaborators
3. They can clone:
   ```bash
   git clone https://github.com/YOUR_USERNAME/naukri-automation.git
   cd naukri-automation
   python setup.py  # They add their own credentials
   ```

## Important Security Notes

### ✅ Safe to share publicly:
- Configuration files (no sensitive data)
- Source code
- Documentation
- Requirements.txt

### ✗ NEVER share:
- .secrets/secrets.json
- Logs with credentials
- Environment variables

### Verify before each push:
```bash
# Show what will be pushed
git diff --cached --name-only

# Make sure no secrets files are listed
# If you see .secrets/secrets.json, don't push!
```

## If You Accidentally Commit Secrets

```bash
# Remove from git (but keep locally)
git rm --cached .secrets/secrets.json

# Commit the removal
git commit -m "Remove: secrets.json (shouldn't be tracked)"

# Push
git push origin main

# Force GitHub to delete (if already pushed)
# WARNING: This rewrites history
git filter-branch --tree-filter 'rm -f .secrets/secrets.json' HEAD
```

## Cloning Later

When you clone this project on a new machine:

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/naukri-automation.git

# Install dependencies
cd naukri-automation
pip install -r requirements.txt

# Setup your secrets (creates .secrets/secrets.json)
python setup.py

# Test it
python src/naukri_main.py
```

## GitHub Features

### Automate with GitHub Actions

You can even run this automatically on GitHub's servers!

Create `.github/workflows/naukri.yml`:

```yaml
name: Naukri Automation

on:
  schedule:
    # Run every hour
    - cron: '0 * * * *'

jobs:
  naukri:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run automation
        env:
          NAUKRI_USERNAME: ${{ secrets.NAUKRI_USERNAME }}
          NAUKRI_PASSWORD: ${{ secrets.NAUKRI_PASSWORD }}
        run: python src/naukri_main.py
```

Then set secrets in GitHub repo settings.

## Best Practices

1. **Commit often** - Small, logical commits
2. **Clear messages** - Explain what changed and why
3. **Review before pushing** - `git diff` before `git push`
4. **Keep secrets separate** - Always use .secrets/ folder
5. **Document changes** - Update README if needed

## Git Commands Cheat Sheet

```bash
# Check status
git status

# See changes
git diff
git diff --cached

# Stage changes
git add .                    # All files
git add config/config.ini    # Specific file

# Commit
git commit -m "Your message"

# Push/Pull
git push origin main
git pull origin main

# View history
git log
git log --oneline

# Undo changes
git checkout filename        # Undo unstaged
git reset HEAD filename      # Unstage file
git revert HEAD~1           # Undo last commit
```

## Need Help?

- GitHub Docs: https://docs.github.com
- Git Tutorial: https://git-scm.com/book
- Common Issues: https://github.com/git-tips/tips

---

**Your code is now version controlled and GitHub-ready!**

Remember: Never commit your secrets! 🔐
