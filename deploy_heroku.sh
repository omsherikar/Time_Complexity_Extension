#!/bin/bash

# TimeComplexity Analyzer - Heroku Deployment Script
# This script deploys the backend API to Heroku

echo "🚀 Deploying TimeComplexity Analyzer API to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please log in to Heroku first:"
    heroku login
fi

# Create Heroku app if it doesn't exist
APP_NAME="timecomplexity-analyzer-api"
echo "📱 Checking Heroku app: $APP_NAME"

if ! heroku apps:info $APP_NAME &> /dev/null; then
    echo "🆕 Creating new Heroku app: $APP_NAME"
    heroku create $APP_NAME
else
    echo "✅ App $APP_NAME already exists"
fi

# Set environment variables
echo "🔧 Setting environment variables..."
heroku config:set ENV=production --app $APP_NAME

# Deploy to Heroku
echo "📤 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku - $(date)"
git push heroku main

# Check if deployment was successful
if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "🌐 API URL: https://$APP_NAME.herokuapp.com"
    echo "🔍 Health check: https://$APP_NAME.herokuapp.com/health"
    
    # Test the API
    echo "🧪 Testing API..."
    curl -s "https://$APP_NAME.herokuapp.com/health" | head -1
    
    echo ""
    echo "🎉 Backend API is now live!"
    echo "📝 Update your extension's API URL to: https://$APP_NAME.herokuapp.com"
else
    echo "❌ Deployment failed. Check the logs:"
    heroku logs --tail --app $APP_NAME
fi
