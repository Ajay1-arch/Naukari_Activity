#!/usr/bin/env python3
"""
Add GitHub Secrets using GitHub API
Requires: GitHub Personal Access Token
"""

import os
import sys
from github import Github
from pathlib import Path


def get_github_token():
    """Get GitHub token from user"""
    print("\n" + "="*60)
    print("GITHUB SECRETS SETUP")
    print("="*60)
    
    print("\n📝 To add secrets, you need a GitHub Personal Access Token")
    print("\n📋 Steps to create token:")
    print("   1. Go to: https://github.com/settings/tokens")
    print("   2. Click: 'Generate new token' → 'Generate new token (classic)'")
    print("   3. Give it a name: 'Naukri Automation'")
    print("   4. Select these scopes:")
    print("      ✓ repo (full control of private repositories)")
    print("   5. Click: 'Generate token'")
    print("   6. Copy the token (you won't see it again!)")
    print("\n")
    
    token = input("Paste your GitHub Personal Access Token here: ").strip()
    
    if not token:
        print("❌ Token is required!")
        sys.exit(1)
    
    return token


def add_secrets(token):
    """Add secrets to GitHub repository"""
    try:
        # Authenticate with GitHub
        g = Github(token)
        
        # Get the repository
        repo = g.get_user("Ajay1-arch").get_repo("Naukari_Activity")
        print(f"\n✅ Connected to repository: {repo.full_name}")
        
        # Load local secrets
        secrets_file = Path(__file__).parent / ".secrets" / "secrets.json"
        import json
        
        with open(secrets_file, 'r') as f:
            local_secrets = json.load(f)
        
        naukri_email = local_secrets.get("naukri", {}).get("username", "")
        naukri_password = local_secrets.get("naukri", {}).get("password", "")
        naukri_mobile = local_secrets.get("naukri", {}).get("mobile", "")
        
        # Secrets to add
        secrets_to_add = {
            "NAUKRI_EMAIL": naukri_email,
            "NAUKRI_PASSWORD": naukri_password,
            "NAUKRI_MOBILE": naukri_mobile,
            "RESUME_PATH": "/tmp/resume.pdf"
        }
        
        print("\n🔐 Adding secrets to GitHub...\n")
        
        for secret_name, secret_value in secrets_to_add.items():
            try:
                repo.create_secret(secret_name, secret_value)
                print(f"✅ Added secret: {secret_name}")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"⚠️  Secret already exists: {secret_name}")
                else:
                    print(f"❌ Error adding {secret_name}: {e}")
        
        print("\n" + "="*60)
        print("✅ Secrets added successfully!")
        print("="*60)
        
        print("\n🚀 Next steps:")
        print("   1. Go to: https://github.com/Ajay1-arch/Naukari_Activity/actions")
        print("   2. Select: 'Naukri Automation - Cloud Scheduler'")
        print("   3. Click: 'Run workflow' → 'Run workflow'")
        print("   4. Watch it execute!\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure:")
        print("   - Token is valid and has 'repo' scope")
        print("   - Repository is accessible")
        print("   - Token hasn't expired")
        return False


def main():
    """Main function"""
    token = get_github_token()
    success = add_secrets(token)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
