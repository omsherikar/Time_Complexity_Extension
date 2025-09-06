# 🚀 TimeComplexity Analyzer - Deployment Guide

This guide will help you deploy the TimeComplexity Analyzer extension for public access.

## 📋 Prerequisites

1. **Chrome Web Store Developer Account** ($5 one-time fee)
2. **Heroku Account** (free tier available)
3. **GitHub Account** (for hosting)

## 🎯 Deployment Options

### Option 1: Chrome Web Store (Recommended)

#### Step 1: Prepare Extension Package

1. **Create a ZIP file** with the following files:
   ```
   extension_1/
   ├── manifest.json
   ├── popup.html
   ├── popup.css
   ├── popup.js
   ├── content.js
   ├── background.js
   ├── icons/
   │   ├── icon16.png
   │   ├── icon48.png
   │   └── icon128.png
   └── README.md
   ```

2. **Test the extension** locally before packaging

#### Step 2: Deploy Backend API

1. **Deploy to Heroku** (see Backend Deployment section below)
2. **Update API URL** in the extension files
3. **Test the deployed API**

#### Step 3: Submit to Chrome Web Store

1. Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
2. Click "Add new item"
3. Upload your ZIP file
4. Fill in the required information:
   - **Name**: TimeComplexity Analyzer
   - **Description**: Analyze time and space complexity of code from 30+ coding platforms
   - **Category**: Developer Tools
   - **Language**: English
   - **Screenshots**: Add screenshots of the extension in action
   - **Privacy Policy**: Required for extensions with permissions

#### Step 4: Required Information for Chrome Web Store

**Store Listing:**
- **Name**: TimeComplexity Analyzer
- **Summary**: AI-powered time complexity analysis for coding platforms
- **Description**: 
  ```
  🚀 Analyze time and space complexity of code instantly on 30+ coding platforms!
  
  ✨ Features:
  • 🤖 ML-Enhanced Analysis (90-95% accuracy)
  • 🌐 Works on LeetCode, Codeforces, HackerRank, and 27+ more platforms
  • 🎯 Selection-based analysis - just select code and click!
  • 🎨 Beautiful modern UI with glass morphism design
  • 📊 Detailed insights with optimization suggestions
  • ⚡ Real-time analysis with confidence scores
  
  🎯 How to Use:
  1. Visit any coding platform
  2. Select/highlight any code
  3. Click the floating "⏱️ Analyze TC" button
  4. View beautiful analysis results!
  
  🌐 Supported Platforms:
  LeetCode, Codeforces, HackerRank, CodeChef, GeeksforGeeks, InterviewBit, 
  Coding Ninjas, Codewars, Exercism, Project Euler, AtCoder, SPOJ, 
  Beecrowd, Luogu, and 20+ more!
  
  Perfect for competitive programmers, coding interview prep, and algorithm learning!
  ```

**Screenshots Needed:**
1. Extension popup interface
2. Floating button on LeetCode
3. Analysis results modal
4. Working on different platforms

**Privacy Policy:**
Create a simple privacy policy stating:
- Extension only processes code you select
- No personal data is collected
- Code is sent to our API for analysis only
- No data is stored permanently

### Option 2: GitHub Pages + Direct Download

#### Step 1: Create GitHub Pages Site

1. Create a new repository: `timecomplexity-analyzer-website`
2. Enable GitHub Pages
3. Create `index.html` with download instructions

#### Step 2: Host Extension Files

1. Create a `releases` folder
2. Upload extension ZIP files for different versions
3. Provide installation instructions

## 🔧 Backend Deployment (Heroku)

### Step 1: Prepare Backend for Heroku

1. **Create `Procfile`**:
   ```
   web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

2. **Create `runtime.txt`**:
   ```
   python-3.11.0
   ```

3. **Update `requirements.txt`** to include production dependencies

### Step 2: Deploy to Heroku

1. **Install Heroku CLI**
2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Heroku app**:
   ```bash
   heroku create timecomplexity-analyzer-api
   ```

4. **Deploy**:
   ```bash
   git add .
   git commit -m "Prepare for Heroku deployment"
   git push heroku main
   ```

5. **Set environment variables** (if needed):
   ```bash
   heroku config:set ENV=production
   ```

### Step 3: Test Deployed API

```bash
curl https://timecomplexity-analyzer-api.herokuapp.com/health
```

## 📦 Extension Packaging

### Create Extension ZIP

```bash
# Create extension package
cd extension_1
zip -r timecomplexity-analyzer-v1.0.0.zip \
  manifest.json \
  popup.html \
  popup.css \
  popup.js \
  content.js \
  background.js \
  icons/ \
  README.md
```

### Test Package

1. Go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the ZIP file
4. Test all functionality

## 🎨 Store Assets Needed

### Icons (Already created)
- 16x16px (icon16.png)
- 48x48px (icon48.png) 
- 128x128px (icon128.png)

### Screenshots Needed
1. **Main Interface**: Extension popup showing analysis
2. **In Action**: Floating button on LeetCode with analysis modal
3. **Multiple Platforms**: Working on different coding sites
4. **Results**: Detailed complexity analysis results

### Promotional Images
- 1280x800px (Chrome Web Store feature graphic)
- 440x280px (Small promotional tile)

## 🔒 Security Considerations

1. **API Security**: Add rate limiting to prevent abuse
2. **CORS**: Properly configure for production
3. **Input Validation**: Sanitize all code inputs
4. **Error Handling**: Graceful error messages

## 📈 Post-Deployment

### Monitoring
1. **API Usage**: Monitor Heroku logs
2. **Extension Installs**: Track in Chrome Web Store dashboard
3. **User Feedback**: Monitor reviews and ratings

### Updates
1. **Version Control**: Use semantic versioning
2. **Changelog**: Document all changes
3. **Rollback Plan**: Keep previous versions available

## 🎯 Success Metrics

- **Downloads**: Target 1000+ installs in first month
- **Ratings**: Maintain 4.5+ star rating
- **Usage**: Track API calls and analysis requests
- **Feedback**: Monitor user reviews and feature requests

## 📞 Support

- **GitHub Issues**: For bug reports and feature requests
- **Email**: For support and business inquiries
- **Documentation**: Keep README updated

---

**Ready to deploy? Start with the Backend Deployment section!** 🚀
