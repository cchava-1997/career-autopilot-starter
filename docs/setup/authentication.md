# Authentication Setup Guide

This guide will help you set up authentication for all external services used by Career Autopilot.

## Quick Setup

Run the automated setup script:

```bash
./scripts/setup_auth.py
```

## Manual Setup

### 1. Overleaf Configuration

#### Get Overleaf API Key
1. Go to [Overleaf](https://www.overleaf.com)
2. Sign in to your account
3. Go to Account Settings → API
4. Generate a new API key
5. Copy the API key

#### Get Project IDs
1. Open your resume projects in Overleaf
2. Copy the project ID from the URL: `https://www.overleaf.com/project/{PROJECT_ID}`
3. Note which project corresponds to each track (PO, PM, TPM)

#### Environment Variables
```bash
OVERLEAF_API_KEY=your_api_key_here
OVERLEAF_PROJECT_PO=your_po_project_id
OVERLEAF_PROJECT_PM=your_pm_project_id
OVERLEAF_PROJECT_TPM=your_tpm_project_id
```

### 2. LinkedIn Configuration

#### Get LinkedIn Credentials
1. Use your LinkedIn email and password
2. For session cookie (optional):
   - Log into LinkedIn in your browser
   - Open Developer Tools (F12)
   - Go to Application/Storage → Cookies
   - Copy the `li_at` cookie value

#### Environment Variables
```bash
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
LINKEDIN_SESSION_COOKIE=your_session_cookie_here
```

### 3. Indeed Configuration

#### Get Indeed Credentials
1. Use your Indeed email and password
2. Create an account if you don't have one

#### Environment Variables
```bash
INDEED_EMAIL=your_email@example.com
INDEED_PASSWORD=your_password
```

### 4. Chrome Profile for ATS

#### Chrome Installation
- Ensure Google Chrome is installed
- Default path on macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

#### Profile Setup
1. Open Chrome and sign into your accounts
2. Install any necessary extensions
3. Set up autofill data
4. Note the profile path

#### Environment Variables
```bash
CHROME_EXECUTABLE_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
CHROME_USER_DATA_DIR=/Users/ptg/Library/Application Support/Google/Chrome
CHROME_PROFILE_PATH=/Users/ptg/Library/Application Support/Google/Chrome/Default
```

### 5. Email Configuration

#### Gmail Setup (Recommended)
1. Enable 2-factor authentication
2. Generate an app password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"

#### Environment Variables
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=your_email@gmail.com
```

## Testing Connections

### Test Overleaf
```bash
curl -X POST "http://localhost:8000/auth/test/overleaf" \
  -H "Content-Type: application/json" \
  -d '{"credentials": {}}'
```

### Test LinkedIn
```bash
curl -X POST "http://localhost:8000/auth/test/linkedin" \
  -H "Content-Type: application/json" \
  -d '{"credentials": {}}'
```

### Test Indeed
```bash
curl -X POST "http://localhost:8000/auth/test/indeed" \
  -H "Content-Type: application/json" \
  -d '{"credentials": {}}'
```

### Test ATS
```bash
curl -X POST "http://localhost:8000/auth/test/ats" \
  -H "Content-Type: application/json" \
  -d '{"credentials": {}}'
```

### Check All Services
```bash
curl -X GET "http://localhost:8000/auth/status"
```

## Security Best Practices

### 1. Environment File Security
- Never commit `.env` file to version control
- Use strong, unique passwords
- Rotate API keys regularly
- Use app-specific passwords when available

### 2. Chrome Profile Security
- Use a dedicated Chrome profile for automation
- Don't store sensitive data in the profile
- Regularly clear cookies and cache
- Use incognito mode when possible

### 3. API Key Management
- Store API keys securely
- Use environment variables
- Implement key rotation
- Monitor API usage

## Troubleshooting

### Common Issues

#### Overleaf API Errors
- Verify API key is correct
- Check project IDs are valid
- Ensure projects are accessible
- Check API rate limits

#### LinkedIn Authentication Issues
- Verify email/password
- Check for 2FA requirements
- Update session cookie if expired
- Use LinkedIn's official API when available

#### Chrome Profile Issues
- Verify Chrome is installed
- Check profile path exists
- Ensure profile is not locked
- Try creating a new profile

#### Email Configuration Issues
- Verify SMTP settings
- Check app password for Gmail
- Test with a simple email client
- Check firewall/network settings

### Debug Mode
Enable debug mode for detailed logging:

```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

### Logs
Check application logs for detailed error information:

```bash
tail -f apps/backend/logs/app.log
```

## Next Steps

1. **Test all connections** using the API endpoints
2. **Verify Chrome profile** works with ATS systems
3. **Test email notifications** work correctly
4. **Set up monitoring** for API usage and errors
5. **Create backups** of your configuration

## Support

If you encounter issues:

1. Check the logs for error details
2. Verify all environment variables are set
3. Test each service individually
4. Check network connectivity
5. Review service-specific documentation

For additional help, refer to the main documentation or create an issue in the project repository.
