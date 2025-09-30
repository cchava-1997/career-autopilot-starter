# LinkedIn OAuth Setup Guide

## Step 1: Create LinkedIn Developer App

1. **Go to LinkedIn Developer Portal**
   - Visit: https://developer.linkedin.com/
   - Sign in with your LinkedIn account

2. **Create New App**
   - Click "Create App" button
   - Fill in the required information:
     - **App name**: `Career Autopilot` (or any name you prefer)
     - **LinkedIn Page**: Select your LinkedIn company page or create a new one
     - **Privacy policy URL**: `http://localhost:3000/privacy` (for development)
     - **App logo**: Upload a logo (optional)

3. **Get App Credentials**
   - After creating the app, go to the "Auth" tab
   - Copy the **Client ID** and **Client Secret**

## Step 2: Configure OAuth Settings

1. **Add Redirect URLs**
   - In the "Auth" tab, scroll down to "OAuth 2.0 settings"
   - Add redirect URL: `http://localhost:8000/auth/linkedin/callback`
   - Click "Add" and then "Update"

2. **Request Permissions**
   - In the "Products" tab, request access to:
     - **Sign In with LinkedIn using OpenID Connect**
     - **Share on LinkedIn** (optional, for posting updates)

## Step 3: Update Environment Variables

1. **Edit your `.env` file**:
   ```bash
   # Replace with your actual LinkedIn app credentials
   LINKEDIN_CLIENT_ID=your_actual_client_id_here
   LINKEDIN_CLIENT_SECRET=your_actual_client_secret_here
   LINKEDIN_REDIRECT_URI=http://localhost:8000/auth/linkedin/callback
   ```

2. **Restart the backend server**:
   ```bash
   # Stop the current server (Ctrl+C)
   # Then restart:
   source .venv/bin/activate
   uvicorn apps.backend.main:app --reload --port 8000
   ```

## Step 4: Test the Integration

1. **Go to Job Sources page**:
   - Visit: http://localhost:3000/sources
   - Click "Login to LinkedIn"
   - You should be redirected to LinkedIn for authentication

2. **Complete OAuth flow**:
   - Sign in with your LinkedIn account
   - Grant permissions to the app
   - You'll be redirected back to the Job Sources page

3. **Test job search**:
   - Once authenticated, click "Search Jobs"
   - Enter keywords like "software engineer"
   - You should see real LinkedIn job listings

## Troubleshooting

### Common Issues:

1. **"Invalid client_id" error**:
   - Make sure you've updated the `.env` file with correct credentials
   - Restart the backend server after updating `.env`

2. **"Redirect URI mismatch" error**:
   - Ensure the redirect URI in LinkedIn app matches exactly: `http://localhost:8000/auth/linkedin/callback`
   - Check for typos in the URL

3. **"Insufficient permissions" error**:
   - Make sure you've requested the correct products in LinkedIn Developer Portal
   - The app needs "Sign In with LinkedIn" permission

4. **Backend not starting**:
   - Check that all environment variables are set correctly
   - Make sure no other process is using port 8000

### Development vs Production:

- **Development**: Use `http://localhost:8000/auth/linkedin/callback`
- **Production**: Use `https://yourdomain.com/auth/linkedin/callback`

## Security Notes

- Never commit your `.env` file to version control
- Keep your Client Secret secure
- Use environment variables in production
- Consider using a secrets management service for production deployments

## Next Steps

Once LinkedIn OAuth is working:
1. Test job search functionality
2. Implement job application automation
3. Add more job sources (Indeed, Glassdoor, etc.)
4. Set up email notifications
5. Configure ATS autofill with Playwright
