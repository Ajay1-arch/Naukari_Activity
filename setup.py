#!/usr/bin/env python3
"""
Setup script for Naukri Automation
Creates secrets.json from template and initializes the project
"""

import json
import shutil
from pathlib import Path
import sys


def setup_project():
    """Setup the project structure and secrets"""
    
    project_root = Path(__file__).parent
    secrets_dir = project_root / ".secrets"
    template_file = secrets_dir / "secrets.template.json"
    secrets_file = secrets_dir / "secrets.json"
    
    print("=" * 80)
    print("Naukri Automation - Setup")
    print("=" * 80)
    
    # Check if secrets.json already exists
    if secrets_file.exists():
        print(f"\n✓ Secrets file already exists at {secrets_file}")
        response = input("Do you want to reconfigure it? (y/n): ").strip().lower()
        if response != 'y':
            print("Setup complete!")
            return
    
    # Check if template exists
    if not template_file.exists():
        print(f"\n✗ Template file not found at {template_file}")
        return
    
    print("\n" + "=" * 80)
    print("Please provide your Naukri credentials and file paths")
    print("=" * 80 + "\n")
    
    # Load template
    with open(template_file, 'r') as f:
        secrets = json.load(f)
    
    # Get input from user
    print("NAUKRI CREDENTIALS:")
    secrets['naukri']['username'] = input("Email/Username: ").strip()
    secrets['naukri']['password'] = input("Password: ").strip()
    secrets['naukri']['mobile'] = input("Mobile Number: ").strip()
    
    print("\nFILE PATHS:")
    original_resume = input("Original Resume Path (e.g., C:\\path\\to\\resume.pdf): ").strip()
    if original_resume:
        secrets['paths']['original_resume'] = original_resume
    
    modified_resume = input("Modified Resume Path (where to save modified resume): ").strip()
    if modified_resume:
        secrets['paths']['modified_resume'] = modified_resume
    
    print("\nCHROME SETTINGS:")
    headless_input = input("Run Chrome in headless mode? (y/n): ").strip().lower()
    secrets['chrome']['headless'] = headless_input == 'y'
    
    # Save secrets
    with open(secrets_file, 'w') as f:
        json.dump(secrets, f, indent=2)
    
    print(f"\n✓ Secrets saved to {secrets_file}")
    print("⚠ WARNING: This file contains sensitive information!")
    print("⚠ Make sure it's in .gitignore (it is by default)")
    
    print("\n" + "=" * 80)
    print("Setup complete!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Run: python src/naukri_main.py  (single execution)")
    print("2. Or run: python src/scheduler.py  (scheduled execution)")
    

if __name__ == "__main__":
    try:
        setup_project()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        sys.exit(1)
