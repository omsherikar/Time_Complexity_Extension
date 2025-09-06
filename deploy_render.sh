#!/bin/bash

# TimeComplexity Analyzer - Render Deployment Script (100% Free)
# This script helps you deploy to Render.com (no credit card required)

echo "🚀 Deploying TimeComplexity Analyzer to Render (100% Free Forever)..."

echo "📋 Manual Deployment Steps:"
echo ""
echo "1. 🌐 Go to https://render.com"
echo "2. 🔐 Sign up with GitHub (no credit card needed)"
echo "3. ➕ Click 'New +' → 'Web Service'"
echo "4. 🔗 Connect repository: omsherikar/Time_Complexity_Extension"
echo "5. ⚙️ Configure service:"
echo "   - Name: timecomplexity-analyzer-api"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT"
echo "   - Python Version: 3.11.0"
echo "6. 🚀 Click 'Create Web Service'"
echo "7. ⏳ Wait for deployment (5-10 minutes)"
echo "8. 🎉 Your API will be live at: https://timecomplexity-analyzer-api.onrender.com"
echo ""

echo "📝 After deployment, update your extension:"
echo "   - Update background.js with the new API URL"
echo "   - Update manifest.json with the new API URL"
echo "   - Package the extension again"
echo ""

echo "✅ Render Benefits:"
echo "   - 100% Free Forever (no time limits)"
echo "   - No credit card required"
echo "   - Automatic deployments from GitHub"
echo "   - Custom domain support"
echo "   - SSL certificate included"
echo "   - 750 hours/month (enough for 24/7)"
echo ""

echo "🔗 Start deployment: https://render.com"
