# GitHub Pages Deployment Guide

This guide will help you deploy your Career Autopilot frontend to GitHub Pages for free hosting.

## Prerequisites

1. A GitHub account
2. Your code pushed to a GitHub repository
3. GitHub Pages enabled on your repository

## Step 1: Push Your Code to GitHub

1. **Create a new repository** on GitHub (if you haven't already):
   - Go to https://github.com/new
   - Name it `career-autopilot-starter` (or any name you prefer)
   - Make it public (required for free GitHub Pages)
   - Don't initialize with README

2. **Push your local code** to GitHub:
   ```bash
   cd /Users/ptg/Documents/PTG\ Docs/career-autopilot-starter
   git init
   git add .
   git commit -m "Initial commit: Career Autopilot application"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/career-autopilot-starter.git
   git push -u origin main
   ```

## Step 2: Enable GitHub Pages

1. **Go to your repository settings**:
   - Navigate to your GitHub repository
   - Click on "Settings" tab
   - Scroll down to "Pages" section

2. **Configure GitHub Pages**:
   - Source: "GitHub Actions"
   - This will use the workflow we created

## Step 3: Configure GitHub Actions

The deployment workflow is already configured in `.github/workflows/deploy-frontend.yml`. It will:

1. Build your Next.js frontend
2. Deploy to GitHub Pages
3. Run automatically on every push to main branch

## Step 4: Update LinkedIn OAuth Settings

Once deployed, update your LinkedIn app settings:

1. **Privacy Policy URL**: 
   ```
   https://YOUR_USERNAME.github.io/career-autopilot-starter/privacy.html
   ```

2. **Redirect URI**:
   ```
   https://YOUR_USERNAME.github.io/career-autopilot-starter/auth/linkedin/callback
   ```

## Step 5: Backend Hosting (Optional)

For a complete deployment, you'll also need to host your backend. Options include:

### Option 1: Heroku (Free tier available)
```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login and create app
heroku login
heroku create your-app-name

# Deploy backend
git subtree push --prefix apps/backend heroku main
```

### Option 2: Railway
- Sign up at https://railway.app
- Connect your GitHub repository
- Deploy the backend service

### Option 3: Render
- Sign up at https://render.com
- Connect your GitHub repository
- Deploy as a web service

## Step 6: Update Environment Variables

Update your `.env` file with production URLs:

```bash
# Frontend URL (GitHub Pages)
FRONTEND_URL=https://YOUR_USERNAME.github.io/career-autopilot-starter

# Backend URL (your hosting service)
BACKEND_URL=https://your-backend-app.herokuapp.com

# LinkedIn OAuth
LINKEDIN_REDIRECT_URI=https://YOUR_USERNAME.github.io/career-autopilot-starter/auth/linkedin/callback
```

## Step 7: Test Your Deployment

1. **Wait for GitHub Actions** to complete (check the "Actions" tab)
2. **Visit your site**: `https://YOUR_USERNAME.github.io/career-autopilot-starter`
3. **Test LinkedIn OAuth** with the new URLs
4. **Verify privacy policy** loads correctly

## Troubleshooting

### Common Issues:

1. **Build fails**: Check GitHub Actions logs for errors
2. **404 errors**: Ensure `basePath` and `assetPrefix` are correct in `next.config.js`
3. **LinkedIn OAuth fails**: Verify redirect URI matches exactly
4. **Backend not accessible**: Check CORS settings and backend URL

### Debug Steps:

1. **Check GitHub Actions logs**:
   - Go to "Actions" tab in your repository
   - Click on the latest workflow run
   - Review build and deployment logs

2. **Test locally with production config**:
   ```bash
   cd apps/frontend
   NODE_ENV=production npm run build
   npm run start
   ```

3. **Verify file paths**:
   - Check that all assets are being served correctly
   - Ensure relative paths work with the basePath

## Custom Domain (Optional)

To use a custom domain:

1. **Add CNAME file** to `apps/frontend/public/`:
   ```
   your-domain.com
   ```

2. **Configure DNS**:
   - Add CNAME record pointing to `YOUR_USERNAME.github.io`

3. **Update GitHub Pages settings**:
   - Add your custom domain in repository settings

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to GitHub
2. **API Keys**: Use GitHub Secrets for production deployments
3. **CORS**: Configure backend to only allow your GitHub Pages domain
4. **HTTPS**: GitHub Pages provides free SSL certificates

## Cost

- **GitHub Pages**: Free for public repositories
- **Backend hosting**: Free tiers available on Heroku, Railway, Render
- **Total cost**: $0 for basic deployment

## Next Steps

After successful deployment:

1. Test all functionality on the live site
2. Update LinkedIn OAuth app with production URLs
3. Set up monitoring and error tracking
4. Configure automatic backups
5. Set up CI/CD for both frontend and backend

Your Career Autopilot application will be live at:
`https://YOUR_USERNAME.github.io/career-autopilot-starter`
