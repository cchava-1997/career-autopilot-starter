#!/usr/bin/env python3
"""
Setup script for Career Autopilot authentication
"""
import os
import sys
import json
import pathlib
from typing import Dict, Any

def create_env_file():
    """Create .env file from template"""
    template_path = pathlib.Path("env.template")
    env_path = pathlib.Path(".env")
    
    if not template_path.exists():
        print("❌ env.template not found")
        return False
    
    if env_path.exists():
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Skipping .env creation")
            return True
    
    # Copy template to .env
    with open(template_path, 'r') as f:
        content = f.read()
    
    with open(env_path, 'w') as f:
        f.write(content)
    
    print("✅ Created .env file from template")
    return True

def setup_overleaf():
    """Setup Overleaf configuration"""
    print("\n🔧 Overleaf Configuration")
    print("=" * 50)
    
    api_key = input("Enter your Overleaf API key (or press Enter to skip): ").strip()
    if not api_key:
        print("⏭️  Skipping Overleaf setup")
        return
    
    print("\nEnter your Overleaf project IDs:")
    po_project = input("PO Project ID (or press Enter to skip): ").strip()
    pm_project = input("PM Project ID (or press Enter to skip): ").strip()
    tpm_project = input("TPM Project ID (or press Enter to skip): ").strip()
    
    # Update .env file
    update_env_file({
        "OVERLEAF_API_KEY": api_key,
        "OVERLEAF_PROJECT_PO": po_project or "",
        "OVERLEAF_PROJECT_PM": pm_project or "",
        "OVERLEAF_PROJECT_TPM": tpm_project or ""
    })
    
    print("✅ Overleaf configuration saved")

def setup_linkedin():
    """Setup LinkedIn configuration"""
    print("\n🔧 LinkedIn Configuration")
    print("=" * 50)
    
    email = input("Enter your LinkedIn email (or press Enter to skip): ").strip()
    if not email:
        print("⏭️  Skipping LinkedIn setup")
        return
    
    password = input("Enter your LinkedIn password: ").strip()
    if not password:
        print("❌ Password required")
        return
    
    session_cookie = input("Enter LinkedIn session cookie (optional): ").strip()
    
    # Update .env file
    update_env_file({
        "LINKEDIN_EMAIL": email,
        "LINKEDIN_PASSWORD": password,
        "LINKEDIN_SESSION_COOKIE": session_cookie or ""
    })
    
    print("✅ LinkedIn configuration saved")

def setup_indeed():
    """Setup Indeed configuration"""
    print("\n🔧 Indeed Configuration")
    print("=" * 50)
    
    email = input("Enter your Indeed email (or press Enter to skip): ").strip()
    if not email:
        print("⏭️  Skipping Indeed setup")
        return
    
    password = input("Enter your Indeed password: ").strip()
    if not password:
        print("❌ Password required")
        return
    
    # Update .env file
    update_env_file({
        "INDEED_EMAIL": email,
        "INDEED_PASSWORD": password
    })
    
    print("✅ Indeed configuration saved")

def setup_chrome_profile():
    """Setup Chrome profile for ATS"""
    print("\n🔧 Chrome Profile Configuration")
    print("=" * 50)
    
    # Check if Chrome is installed
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser"
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if pathlib.Path(path).exists():
            chrome_found = True
            print(f"✅ Found Chrome at: {path}")
            break
    
    if not chrome_found:
        print("⚠️  Chrome not found in standard locations")
        custom_path = input("Enter Chrome executable path (or press Enter to skip): ").strip()
        if custom_path:
            chrome_paths = [custom_path]
    
    # Get user data directory
    user_data_dir = input("Enter Chrome user data directory (or press Enter for default): ").strip()
    if not user_data_dir:
        user_data_dir = "/Users/ptg/Library/Application Support/Google/Chrome"
    
    profile_path = input("Enter Chrome profile path (or press Enter for default): ").strip()
    if not profile_path:
        profile_path = f"{user_data_dir}/Default"
    
    # Update .env file
    update_env_file({
        "CHROME_EXECUTABLE_PATH": chrome_paths[0] if chrome_paths else "",
        "CHROME_USER_DATA_DIR": user_data_dir,
        "CHROME_PROFILE_PATH": profile_path
    })
    
    print("✅ Chrome profile configuration saved")

def setup_email():
    """Setup email configuration"""
    print("\n🔧 Email Configuration")
    print("=" * 50)
    
    smtp_host = input("Enter SMTP host (or press Enter for Gmail): ").strip()
    if not smtp_host:
        smtp_host = "smtp.gmail.com"
    
    smtp_port = input("Enter SMTP port (or press Enter for 587): ").strip()
    if not smtp_port:
        smtp_port = "587"
    
    username = input("Enter email username: ").strip()
    if not username:
        print("❌ Email username required")
        return
    
    password = input("Enter email password/app password: ").strip()
    if not password:
        print("❌ Email password required")
        return
    
    email_from = input("Enter from email (or press Enter to use username): ").strip()
    if not email_from:
        email_from = username
    
    email_to = input("Enter to email (or press Enter to use username): ").strip()
    if not email_to:
        email_to = username
    
    # Update .env file
    update_env_file({
        "SMTP_HOST": smtp_host,
        "SMTP_PORT": smtp_port,
        "SMTP_USERNAME": username,
        "SMTP_PASSWORD": password,
        "EMAIL_FROM": email_from,
        "EMAIL_TO": email_to
    })
    
    print("✅ Email configuration saved")

def update_env_file(updates: Dict[str, str]):
    """Update .env file with new values"""
    env_path = pathlib.Path(".env")
    if not env_path.exists():
        print("❌ .env file not found")
        return
    
    # Read current content
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update lines
    for key, value in updates.items():
        found = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                found = True
                break
        
        if not found:
            lines.append(f"{key}={value}\n")
    
    # Write back
    with open(env_path, 'w') as f:
        f.writelines(lines)

def main():
    """Main setup function"""
    print("🚀 Career Autopilot Authentication Setup")
    print("=" * 50)
    
    # Change to project root
    script_dir = pathlib.Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Create .env file
    if not create_env_file():
        return
    
    # Setup services
    services = [
        ("Overleaf", setup_overleaf),
        ("LinkedIn", setup_linkedin),
        ("Indeed", setup_indeed),
        ("Chrome Profile", setup_chrome_profile),
        ("Email", setup_email)
    ]
    
    for service_name, setup_func in services:
        try:
            setup_func()
        except KeyboardInterrupt:
            print("\n\n⏹️  Setup interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error setting up {service_name}: {e}")
            continue
    
    print("\n🎉 Authentication setup complete!")
    print("\nNext steps:")
    print("1. Review your .env file")
    print("2. Test connections using the API endpoints")
    print("3. Start the application with: ./scripts/dev.sh")

if __name__ == "__main__":
    main()
