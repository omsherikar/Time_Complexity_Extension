#!/bin/bash

# TimeComplexity Analyzer - GitHub Pages Setup Script
# This script helps you set up GitHub Pages for hosting the extension website

echo "🌐 Setting up GitHub Pages for TimeComplexity Analyzer..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please run this from your project root."
    exit 1
fi

# Get repository URL
REPO_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REPO_URL" ]; then
    echo "❌ No remote repository found. Please add a remote origin first."
    exit 1
fi

echo "📁 Repository: $REPO_URL"

# Create website directory if it doesn't exist
mkdir -p website

# Create a simple index.html if it doesn't exist
if [ ! -f "website/index.html" ]; then
    echo "📝 Creating website/index.html..."
    cat > website/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TimeComplexity Analyzer - Chrome Extension</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 40px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { color: #333; font-size: 2.5rem; margin-bottom: 10px; }
        .download-btn { display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 15px 30px; border-radius: 50px; text-decoration: none; font-weight: 600; margin: 10px; transition: all 0.3s ease; }
        .download-btn:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3); }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
        .feature { background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea; }
        .instructions { background: #e3f2fd; border: 1px solid #bbdefb; border-radius: 10px; padding: 20px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⏱️ TimeComplexity Analyzer</h1>
            <p>AI-powered time complexity analysis for coding platforms</p>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="https://github.com/$(echo $REPO_URL | sed 's/.*github.com[:/]\([^/]*\/[^/]*\)\.git.*/\1/')/releases/latest" class="download-btn">
                📥 Download Extension
            </a>
            <a href="https://github.com/$(echo $REPO_URL | sed 's/.*github.com[:/]\([^/]*\/[^/]*\)\.git.*/\1/')" class="download-btn">
                🔗 View on GitHub
            </a>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>🤖 ML-Enhanced Analysis</h3>
                <p>90-95% accuracy using ensemble machine learning models.</p>
            </div>
            <div class="feature">
                <h3>🌐 Universal Compatibility</h3>
                <p>Works on 30+ coding platforms including LeetCode, Codeforces, and HackerRank.</p>
            </div>
            <div class="feature">
                <h3>🎯 Selection-Based Analysis</h3>
                <p>Simply select any code and click the floating button for instant analysis.</p>
            </div>
            <div class="feature">
                <h3>🎨 Beautiful UI</h3>
                <p>Modern glass morphism design with smooth animations.</p>
            </div>
        </div>
        
        <div class="instructions">
            <h3>📋 How to Install</h3>
            <ol>
                <li>Download the extension ZIP file from the link above</li>
                <li>Extract the ZIP file to a folder on your computer</li>
                <li>Open Chrome and go to <code>chrome://extensions/</code></li>
                <li>Enable "Developer mode" (toggle in top-right corner)</li>
                <li>Click "Load unpacked" and select the extracted folder</li>
                <li>Visit any coding platform and start analyzing!</li>
            </ol>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #666;">
            <p>Made with ❤️ for the coding community</p>
        </div>
    </div>
</body>
</html>
EOF
fi

# Create a simple README for the website
cat > website/README.md << 'EOF'
# TimeComplexity Analyzer Website

This is the website for the TimeComplexity Analyzer Chrome extension.

## Setup

1. Enable GitHub Pages in your repository settings
2. Select "Deploy from a branch"
3. Choose "main" branch
4. Your site will be available at: `https://yourusername.github.io/repository-name`

## Files

- `index.html` - Main website page
- `README.md` - This file

## Customization

Edit `index.html` to customize the website content, styling, and links.
EOF

echo "✅ Website files created in website/ directory"
echo ""
echo "📋 Next steps:"
echo "1. Commit and push the website files:"
echo "   git add website/"
echo "   git commit -m 'Add website for GitHub Pages'"
echo "   git push origin main"
echo ""
echo "2. Enable GitHub Pages:"
echo "   - Go to your repository on GitHub"
echo "   - Click Settings → Pages"
echo "   - Select 'Deploy from a branch'"
echo "   - Choose 'main' branch"
echo "   - Click Save"
echo ""
echo "3. Your website will be available at:"
echo "   https://$(echo $REPO_URL | sed 's/.*github.com[:/]\([^/]*\/[^/]*\)\.git.*/\1/' | tr '[:upper:]' '[:lower:]')"
echo ""
echo "🎉 Website setup complete!"
