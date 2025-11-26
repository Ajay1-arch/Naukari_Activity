#!/usr/bin/env python3
"""
Add GitHub Secrets for Cloud Automation
This script adds your Naukri credentials as GitHub Secrets
"""

import json
import subprocess
import sys
from pathlib import Path


def load_local_secrets():
    """Load secrets from local .secrets/secrets.json"""
    secrets_file = Path(__file__).parent / ".secrets" / "secrets.json"
    
    if not secrets_file.exists():
        print("❌ Error: .secrets/secrets.json not found!")
        print("   Please run: python setup.py")
        sys.exit(1)
    
    try:
        with open(secrets_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading secrets: {e}")
        sys.exit(1)


def add_github_secret(secret_name, secret_value, repo_path):
    """Add a secret to GitHub using GitHub CLI"""
    try:
        # Using GitHub CLI (gh) to add secret
        cmd = [
            "gh", "secret", "set", secret_name,
            "--body", str(secret_value),
            "-R", repo_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Added secret: {secret_name}")
            return True
        else:
            print(f"❌ Failed to add secret: {secret_name}")
            print(f"   Error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) not found!")
        print("   Install it from: https://cli.github.com/")
        return False


def main():
    """Main function"""
    print("\n" + "="*60)
    print("GitHub Secrets Setup for Cloud Automation")
    print("="*60 + "\n")
    
    # Load local secrets
    print("📂 Loading local secrets...")
    secrets = load_local_secrets()
    
    naukri_email = secrets.get("naukri", {}).get("username", "")
    naukri_password = secrets.get("naukri", {}).get("password", "")
    naukri_mobile = secrets.get("naukri", {}).get("mobile", "")
    
    # Display secrets (partially masked)
    print(f"   📧 Email: {naukri_email[:10]}***@gmail.com")
    print(f"   🔐 Password: {naukri_password[:3]}***{naukri_password[-2:]}")
    print(f"   📱 Mobile: {naukri_mobile[:4]}****{naukri_mobile[-3:]}")
    
    # Confirm before adding
    print("\n⚠️  These secrets will be added to GitHub (encrypted)")
    confirm = input("Continue? (yes/no): ").strip().lower()
    
    if confirm != "yes":
        print("❌ Cancelled")
        sys.exit(0)
    
    # Repository info
    repo_owner = "Ajay1-arch"
    repo_name = "Naukari_Activity"
    repo_path = f"{repo_owner}/{repo_name}"
    
    print(f"\n🔐 Adding secrets to: {repo_path}\n")
    
    # Add secrets
    success_count = 0
    
    secrets_to_add = {
        "NAUKRI_EMAIL": naukri_email,
        "NAUKRI_PASSWORD": naukri_password,
        "NAUKRI_MOBILE": naukri_mobile,
        "RESUME_PATH": "/tmp/resume.pdf"
    }
    
    for secret_name, secret_value in secrets_to_add.items():
        if add_github_secret(secret_name, secret_value, repo_path):
            success_count += 1
    
    # Summary
    print("\n" + "="*60)
    if success_count == len(secrets_to_add):
        print(f"✅ Successfully added all {success_count} secrets!")
        print("\n🚀 Next steps:")
        print("   1. Go to: https://github.com/Ajay1-arch/Naukari_Activity/actions")
        print("   2. Select: 'Naukri Automation - Cloud Scheduler'")
        print("   3. Click: 'Run workflow' → 'Run workflow'")
        print("\n✨ Your cloud automation will start running!")
    else:
        print(f"⚠️  Added {success_count}/{len(secrets_to_add)} secrets")
        print("\n💡 If GitHub CLI is not installed:")
        print("   1. Install from: https://cli.github.com/")
        print("   2. Run: gh auth login")
        print("   3. Then run this script again")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
