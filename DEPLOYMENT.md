# Deploying to Streamlit Cloud

## Prerequisites
- GitHub account with your code pushed
- Streamlit Cloud account (free)

## Step-by-Step Deployment Guide

### 1. Sign Up for Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up with GitHub"
3. Authorize Streamlit Cloud to access your GitHub repositories

### 2. Deploy Your App
1. Click "New app" button
2. Select your repository: `parbatpaudel/scropper`
3. Select the branch: `master`
4. Set the main file path: `app.py`
5. Click "Deploy!"

### 3. Configure Environment Variables
**IMPORTANT:** Before your app will work properly, you need to add your Groq API key:

1. Click on the **⋮ menu** (three dots) in the top right corner of your deployed app
2. Select **"Settings"**
3. Go to the **"Secrets"** section
4. Add your secrets in TOML format:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
GROQ_MODEL = "mixtral-8x7b-32768"
MAX_PAGES_TO_SCRAPE = 50
SCRAPE_DELAY_SECONDS = 1
```

5. Click **"Save"**
6. Your app will automatically reboot with the new configuration

### 4. Get Your Groq API Key
If you don't have a Groq API key yet:
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to Streamlit secrets

### 5. Wait for Deployment
- Streamlit Cloud will install all dependencies from `requirements.txt`
- It will also install system packages from `packages.txt` (Chromium for web scraping)
- The initial deployment may take 3-5 minutes
- You'll see build logs in real-time

### 6. Access Your App
Once deployed, you'll get a URL like:
```
https://[your-app-name].streamlit.app
```

Share this URL with anyone to give them access to your web scraper!

## Configuration Files

Your app is configured with these files:

### `requirements.txt`
Contains all Python dependencies (already in your repo)

### `packages.txt`
Contains system dependencies for Selenium/Chromium (already in your repo)

### `.streamlit/config.toml` (Optional)
You can create this file to customize Streamlit settings:

```toml
[theme]
primaryColor = "#F97316"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F8FAFC"
textColor = "#1E293B"
font = "sans serif"

[server]
maxUploadSize = 200
```

## Troubleshooting

### App Won't Start
- Check the build logs for errors
- Verify all dependencies in `requirements.txt` are compatible
- Make sure `GROQ_API_KEY` is set in secrets

### Selenium Errors
- The `packages.txt` file should contain:
  ```
  chromium
  chromium-driver
  ```
- The code automatically detects Chromium on Streamlit Cloud

### API Key Issues
- Double-check the API key in secrets (no quotes needed in the value)
- Make sure there are no extra spaces
- Verify the key is valid at console.groq.com

### Memory Limits
- Free Streamlit Cloud apps have 1GB RAM limit
- Consider reducing `MAX_PAGES_TO_SCRAPE` if you hit memory limits
- Scraping fewer pages at once can help

## Advanced Configuration

### Custom Domain
1. Go to app settings
2. Click on "Custom subdomain"
3. Enter your preferred subdomain

### App Sleeping
- Free apps sleep after 7 days of inactivity
- They wake up automatically when someone visits
- Wake-up takes ~30 seconds

### Update Your App
When you push changes to GitHub:
1. Streamlit Cloud will automatically detect changes
2. Click "Reboot app" to deploy updates
3. Or enable auto-reboot in settings

## Resource Limits (Free Tier)
- 1 GB RAM
- 1 CPU core
- No limit on app usage
- Apps sleep after 7 days of no activity

## Support
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub Issues](https://github.com/parbatpaudel/scropper/issues)

---

**Your app repository:** https://github.com/parbatpaudel/scropper
**Deploy at:** https://share.streamlit.io
