#!/usr/bin/env python3
"""
Simple test to verify the project setup is correct
"""

import sys
from pathlib import Path

def test_structure():
    """Test project structure"""
    print("Testing Naukri Automation Project Structure...\n")
    
    project_root = Path(__file__).parent
    
    # Check directories
    dirs_to_check = [
        '.secrets',
        'config',
        'src',
        'logs',
    ]
    
    print("✓ Checking directories...")
    for dir_name in dirs_to_check:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ MISSING")
            return False
    
    # Check files
    files_to_check = [
        ('.gitignore', 'root'),
        ('requirements.txt', 'root'),
        ('setup.py', 'root'),
        ('README.md', 'root'),
        ('QUICK_START.md', 'root'),
        ('.secrets/secrets.template.json', 'secrets'),
        ('config/config.ini', 'config'),
        ('src/config_loader.py', 'source'),
        ('src/scheduler.py', 'source'),
        ('src/naukri_main.py', 'source'),
    ]
    
    print("\n✓ Checking files...")
    for file_name, category in files_to_check:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ {file_name} MISSING")
            return False
    
    # Check .secrets/secrets.json (should NOT exist yet)
    secrets_file = project_root / '.secrets' / 'secrets.json'
    if not secrets_file.exists():
        print(f"  ℹ .secrets/secrets.json (not created yet - run setup.py)")
    else:
        print(f"  ✓ .secrets/secrets.json (already configured)")
    
    return True


def test_python_packages():
    """Test if required packages are installed"""
    print("\n✓ Checking Python packages...")
    
    packages = ['selenium', 'pypdf', 'reportlab']
    missing = []
    
    for package in packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠ Run: pip install -r requirements.txt")
        return False
    
    return True


def main():
    """Run all tests"""
    print("=" * 70)
    print("NAUKRI AUTOMATION - PROJECT VERIFICATION")
    print("=" * 70)
    
    structure_ok = test_structure()
    packages_ok = test_python_packages()
    
    print("\n" + "=" * 70)
    
    if structure_ok and packages_ok:
        print("✓ PROJECT STRUCTURE OK!")
        print("\nNext steps:")
        print("1. Run: python setup.py")
        print("2. Run: python src/naukri_main.py")
        print("3. Check: logs/naukri.log")
        print("=" * 70)
        return 0
    else:
        print("✗ PROJECT STRUCTURE ISSUES FOUND")
        print("\nFix:")
        print("- Ensure all files exist")
        print("- Run: pip install -r requirements.txt")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
