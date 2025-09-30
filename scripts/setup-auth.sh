#!/bin/bash

# Career Autopilot Authentication Setup Script
# This script helps you set up authentication for all external services

set -e

echo "🔐 Career Autopilot Authentication Setup"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🔧 Authentication Setup Checklist"
echo "================================"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required tools
echo "📋 Checking required tools..."

if command_exists google-chrome || command_exists chromium-browser; then
    echo "✅ Chrome/Chromium browser found"
else
    echo "❌ Chrome/Chromium browser not found"
    echo "   Please install Chrome for ATS autofill functionality"
fi

if command_exists python3; then
    echo "✅ Python 3 found"
else
    echo "❌ Python 3 not found"
    echo "   Please install Python 3.10+"
fi

if command_exists node; then
    echo "✅ Node.js found"
else
    echo "❌ Node.js not found"
    echo "   Please install Node.js 18+"
fi

echo ""
echo "🌐 Service Setup Instructions"
echo "============================"
echo ""

echo "1. 📄 OVERLEAF (Resume PDF Generation)"
echo "   • Go to: https://www.overleaf.com"
echo "   • Create account and projects for PO/PM/TPM tracks"
echo "   • Get API key from Account Settings → API"
echo "   • Add to .env: OVERLEAF_API_KEY=sk-your-key-here"
echo ""

echo "2. 💼 LINKEDIN (Professional Networking)"
echo "   • Go to: https://www.linkedin.com"
echo "   • Log into your account"
echo "   • Complete your profile"
echo "   • No API key needed (uses browser session)"
echo ""

echo "3. 🔍 INDEED (Job Search)"
echo "   • Go to: https://www.indeed.com"
echo "   • Create account and upload resume"
echo "   • Set up job alerts"
echo "   • No API key needed (uses browser session)"
echo ""

echo "4. 🌐 CHROME PROFILE (ATS Autofill)"
echo "   • Open Chrome → Settings → Profiles"
echo "   • Create new profile: 'Career Autopilot'"
echo "   • Log into ATS systems: Workday, Greenhouse, Lever, Ashby"
echo "   • Save passwords and enable autofill"
echo "   • Add to .env: CHROME_USER_DATA_DIR=/path/to/profile"
echo ""

echo "5. 📧 GMAIL (Email Management)"
echo "   • Use your primary Gmail account"
echo "   • Enable 2FA for security"
echo "   • Create email templates"
echo "   • No API key needed (uses browser session)"
echo ""

echo "6. 📅 CALENDAR (Follow-up Scheduling)"
echo "   • Use Google Calendar or Apple Calendar"
echo "   • Create dedicated calendar for job search"
echo "   • Set up notification preferences"
echo "   • No API key needed (uses system calendar)"
echo ""

echo "🔧 Configuration Steps"
echo "====================="
echo ""

echo "1. Edit .env file with your settings:"
echo "   nano .env"
echo ""

echo "2. Test your configuration:"
echo "   ./scripts/test-auth.sh"
echo ""

echo "3. Start the application:"
echo "   ./scripts/dev.sh"
echo ""

echo "4. Open Settings page in the app to test connections"
echo ""

echo "📚 Additional Resources"
echo "======================"
echo ""

echo "• Authentication Setup Guide: docs/setup/authentication_setup.md"
echo "• Overleaf API Docs: https://www.overleaf.com/learn/how-to/How_to_use_Overleaf_with_Git"
echo "• Chrome Profile Management: https://support.google.com/chrome/answer/2364824"
echo "• ATS System Documentation: https://www.workday.com/en-us/products/human-capital-management/recruiting.html"
echo ""

echo "🚨 Security Reminders"
echo "===================="
echo ""

echo "• Never commit API keys to version control"
echo "• Use environment variables for all sensitive data"
echo "• Enable 2FA on all accounts"
echo "• Use dedicated Chrome profile for job applications"
echo "• Regularly rotate API keys"
echo ""

echo "✅ Setup instructions complete!"
echo ""
echo "Next steps:"
echo "1. Follow the service setup instructions above"
echo "2. Configure your .env file"
echo "3. Test your setup with: ./scripts/test-auth.sh"
echo "4. Start the application with: ./scripts/dev.sh"
echo ""
echo "Happy job hunting! 🎯"
