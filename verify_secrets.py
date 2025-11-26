#!/usr/bin/env python3
"""
Verify GitHub Secrets are configured correctly
"""

import json
from pathlib import Path


def check_workflow_file():
    """Check that workflow file references the correct secrets"""
    workflow_file = Path(__file__).parent / ".github" / "workflows" / "naukri-scheduler.yml"
    
    if not workflow_file.exists():
        print("❌ Workflow file not found!")
        return False
    
    with open(workflow_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_secrets = [
        'NAUKRI_EMAIL',
        'NAUKRI_PASSWORD',
        'NAUKRI_MOBILE',
        'RESUME_PATH'
    ]
    
    print("\n📋 Checking Workflow Configuration...")
    print("="*60)
    
    all_found = True
    for secret in required_secrets:
        if secret in content:
            print(f"✅ Secret '{secret}' referenced in workflow")
        else:
            print(f"❌ Secret '{secret}' NOT found in workflow")
            all_found = False
    
    return all_found


def check_local_config():
    """Check local configuration files"""
    print("\n📂 Checking Local Configuration...")
    print("="*60)
    
    files_to_check = [
        (".secrets/secrets.json", "Local secrets"),
        ("config/config.ini", "Configuration"),
        (".github/workflows/naukri-scheduler.yml", "GitHub Actions workflow"),
        ("src/naukri_main.py", "Main automation script"),
        ("src/config_loader.py", "Config loader"),
    ]
    
    all_exist = True
    for filepath, description in files_to_check:
        path = Path(__file__).parent / filepath
        if path.exists():
            print(f"✅ {description:<30} {filepath}")
        else:
            print(f"❌ {description:<30} {filepath}")
            all_exist = False
    
    return all_exist


def show_next_steps():
    """Show next steps"""
    print("\n🚀 Next Steps to Verify...")
    print("="*60)
    print("""
1. Go to GitHub: https://github.com/Ajay1-arch/Naukari_Activity/settings/secrets/actions
2. You should see 4 secrets listed:
   ✓ NAUKRI_EMAIL
   ✓ NAUKRI_PASSWORD
   ✓ NAUKRI_MOBILE
   ✓ RESUME_PATH

3. Go to Actions tab: https://github.com/Ajay1-arch/Naukari_Activity/actions
4. Select "Naukri Automation - Cloud Scheduler"
5. Click "Run workflow" → "Run workflow"
6. Watch it execute in real-time!

If workflow fails, check:
- All 4 secrets are present in Settings → Secrets
- Secret names match exactly (case-sensitive)
- Values are correct
- Workflow file is committed to GitHub
    """)


def main():
    print("\n" + "="*60)
    print("NAUKRI AUTOMATION - SECRETS VERIFICATION")
    print("="*60)
    
    workflow_ok = check_workflow_file()
    config_ok = check_local_config()
    
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    if workflow_ok and config_ok:
        print("✅ All local configurations are correct!")
        print("✅ Workflow references all required secrets")
        print("\n📋 Now you need to manually verify secrets on GitHub:")
        print("   Go to: https://github.com/Ajay1-arch/Naukari_Activity/settings/secrets/actions")
        print("   You should see 4 secrets listed (values hidden for security)")
    else:
        print("⚠️  Some issues found - please check above")
    
    show_next_steps()
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
