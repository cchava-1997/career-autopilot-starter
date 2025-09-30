# Authentication Setup Guide

This guide will help you set up authentication for all the external services used by Career Autopilot.

## 🔐 Required Services & Authentication

### 1. Overleaf (Resume PDF Generation)

**Purpose**: Generate A4 PDF resumes from LaTeX templates

**Setup Steps**:
1. Go to [Overleaf](https://www.overleaf.com) and create an account
2. Create a new project for each track (PO, PM, TPM)
3. Get your API key:
   - Go to Account Settings → API
   - Generate a new API key
   - Copy the key (starts with `sk-`)

**Configuration**:
- Add API key to `.env` file
- Add project IDs for each track
- Test connection in Settings page

**Template Requirements**:
- A4 page size
- Tight whitespace (1-2 pages max)
- Include `\input{_layout_autogen.tex}` for dynamic content
- Support for track-specific content

### 2. LinkedIn (Professional Networking)

**Purpose**: Job search, networking, outreach

**Setup Steps**:
1. Log into LinkedIn in your browser
2. Ensure you're logged in to the same browser profile used by Career Autopilot
3. Verify your profile is complete and up-to-date

**Configuration**:
- No API key needed (uses browser session)
- Ensure Chrome profile path is correct in settings
- Test LinkedIn access in Settings page

**Usage**:
- Job search and application tracking
- Outreach message generation
- Profile viewing and connection requests

### 3. Indeed (Job Search)

**Purpose**: Job board for finding opportunities

**Setup Steps**:
1. Create Indeed account at [indeed.com](https://www.indeed.com)
2. Complete your profile with resume
3. Set up job alerts for your target roles

**Configuration**:
- No API key needed (uses browser session)
- Add Indeed to job sources in the app
- Test accessibility in Settings page

### 4. Chrome Profile (ATS Autofill)

**Purpose**: Automated form filling for ATS systems

**Setup Steps**:
1. Create a dedicated Chrome profile for job applications
2. Log into all ATS systems you use:
   - Workday
   - Greenhouse
   - Lever
   - Ashby
   - Company-specific ATS
3. Save login credentials in Chrome
4. Test form filling on a sample application

**Configuration**:
- Set Chrome user data directory in settings
- Configure profile fields (name, email, phone)
- Test Chrome profile access in Settings page

**ATS Systems to Configure**:
- **Workday**: Most common enterprise ATS
- **Greenhouse**: Popular startup ATS
- **Lever**: Common in tech companies
- **Ashby**: Growing in popularity
- **BambooHR**: Smaller companies
- **JazzHR**: Mid-size companies

### 5. Gmail (Email Management)

**Purpose**: Send outreach emails and manage communications

**Setup Steps**:
1. Use your primary Gmail account
2. Enable 2FA for security
3. Create email templates for outreach
4. Set up email signatures

**Configuration**:
- No API key needed (uses browser session)
- Ensure Gmail is accessible in Chrome profile
- Test email draft creation in Settings page

### 6. Calendar (Follow-up Scheduling)

**Purpose**: Schedule follow-up reminders

**Setup Steps**:
1. Use Google Calendar or Apple Calendar
2. Create a dedicated calendar for job search
3. Set up notification preferences

**Configuration**:
- No API key needed (uses system calendar)
- Test calendar access in Settings page

## 🛠️ Setup Checklist

### Phase 1: Core Services
- [ ] Overleaf account and API key
- [ ] Chrome profile with ATS logins
- [ ] LinkedIn account and profile
- [ ] Indeed account and profile

### Phase 2: ATS Systems
- [ ] Workday login
- [ ] Greenhouse login
- [ ] Lever login
- [ ] Ashby login
- [ ] Company-specific ATS logins

### Phase 3: Communication
- [ ] Gmail account setup
- [ ] Email templates created
- [ ] Calendar integration
- [ ] Phone number for applications

### Phase 4: Testing
- [ ] Test Overleaf PDF generation
- [ ] Test Chrome profile access
- [ ] Test LinkedIn job search
- [ ] Test Indeed job search
- [ ] Test ATS form filling
- [ ] Test email draft creation

## 🔧 Configuration Steps

### 1. Environment Variables (.env)
```bash
# Overleaf Configuration
OVERLEAF_API_KEY=sk-your-api-key-here
OVERLEAF_PROJECT_PO=your-po-project-id
OVERLEAF_PROJECT_PM=your-pm-project-id
OVERLEAF_PROJECT_TPM=your-tpm-project-id

# Chrome Profile
CHROME_USER_DATA_DIR=/Users/yourusername/Library/Application Support/Google/Chrome/Profile 1

# Profile Fields
PROFILE_NAME="Your Full Name"
PROFILE_EMAIL="your.email@example.com"
PROFILE_PHONE="+1 (555) 123-4567"

# File Paths
TRACKER_PATH=/Users/yourusername/Documents/career_autopilot_tracker.xlsx
APPLY_PACK_DIR=/Users/yourusername/Documents/career_autopilot/applications
RESUME_DIR=/Users/yourusername/Documents/career_autopilot/resumes
```

### 2. Chrome Profile Setup
1. Open Chrome
2. Go to Settings → Profiles
3. Create new profile: "Career Autopilot"
4. Log into all required services
5. Save passwords and enable autofill
6. Note the profile path for configuration

### 3. Overleaf Project Setup
1. Create new project for each track
2. Use A4 template with tight margins
3. Include dynamic content placeholders
4. Test PDF generation
5. Note project IDs for configuration

## 🧪 Testing Your Setup

### Test Overleaf Connection
```bash
curl -X POST "http://localhost:8000/settings/test-overleaf"
```

### Test Chrome Profile
```bash
curl -X POST "http://localhost:8000/settings/test-chrome"
```

### Test LaTeX Build
```bash
curl -X POST "http://localhost:8000/settings/test-latex"
```

## 🚨 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Enable 2FA** on all accounts
4. **Use dedicated Chrome profile** for job applications
5. **Regularly rotate API keys**
6. **Monitor account activity** for suspicious behavior

## 🔄 Maintenance

### Weekly
- Check Overleaf project status
- Verify Chrome profile accessibility
- Test ATS form filling
- Review email templates

### Monthly
- Rotate API keys
- Update resume templates
- Review job source effectiveness
- Check calendar integration

### Quarterly
- Audit account security
- Update ATS system configurations
- Review and update email templates
- Test all integrations

## 🆘 Troubleshooting

### Common Issues

1. **Overleaf API Key Invalid**
   - Check key format (starts with `sk-`)
   - Verify key is active in Overleaf
   - Check project IDs are correct

2. **Chrome Profile Not Found**
   - Verify profile path is correct
   - Check profile exists in Chrome
   - Ensure profile has necessary permissions

3. **ATS Form Filling Fails**
   - Check if logged into ATS
   - Verify form selectors are current
   - Test manual form filling first

4. **LinkedIn Access Denied**
   - Check if logged into LinkedIn
   - Verify profile is complete
   - Check for rate limiting

### Getting Help

1. Check application logs: `apps/backend/logs/app.log`
2. Test individual components in Settings page
3. Verify environment variables are set correctly
4. Check browser console for errors
5. Review API documentation for each service

## 📚 Additional Resources

- [Overleaf API Documentation](https://www.overleaf.com/learn/how-to/How_to_use_Overleaf_with_Git)
- [LinkedIn Developer Documentation](https://docs.microsoft.com/en-us/linkedin/)
- [Chrome Profile Management](https://support.google.com/chrome/answer/2364824)
- [ATS System Documentation](https://www.workday.com/en-us/products/human-capital-management/recruiting.html)
