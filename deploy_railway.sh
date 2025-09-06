#!/bin/bash

# TimeComplexity Analyzer - Railway Deployment Script (Free)
# This script deploys the backend API to Railway's free tier

echo "🚀 Deploying TimeComplexity Analyzer API to Railway (Free Tier)..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Check if user is logged in to Railway
if ! railway whoami &> /dev/null; then
    echo "🔐 Please log in to Railway first:"
    railway login
fi

# Initialize Railway project if not already done
if [ ! -f "railway.json" ]; then
    echo "🆕 Initializing Railway project..."
    railway init
fi

# Deploy to Railway
echo "📤 Deploying to Railway..."
railway up

# Check if deployment was successful
if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    
    # Get the deployed URL
    RAILWAY_URL=$(railway domain)
    echo "🌐 API URL: https://$RAILWAY_URL"
    echo "🔍 Health check: https://$RAILWAY_URL/health"
    
    # Test the API
    echo "🧪 Testing API..."
    curl -s "https://$RAILWAY_URL/health" | head -1
    
    echo ""
    echo "🎉 Backend API is now live on Railway!"
    echo "📝 Update your extension's API URL to: https://$RAILWAY_URL"
    echo ""
    echo "💡 Next steps:"
    echo "1. Update background.js with the new API URL"
    echo "2. Package the extension: ./package_extension.sh"
    echo "3. Create a GitHub release with the ZIP file"
    echo "4. Deploy website to GitHub Pages"
else
    echo "❌ Deployment failed. Check the logs:"
    railway logs
fi
