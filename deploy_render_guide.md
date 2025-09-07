# 🆓 Deploy to Render (100% Free Forever)

Render offers a completely free tier with no time limits and no credit card required.

## Step 1: Deploy Backend to Render

1. **Go to**: https://render.com
2. **Sign up** with GitHub (no credit card needed)
3. **Click "New +"** → **"Web Service"**
4. **Connect your GitHub repository**: `omsherikar/Time_Complexity_Extension`
5. **Configure the service**:
   - **Name**: `timecomplexity-analyzer-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Python Version**: `3.11.0`
6. **Click "Create Web Service"**
7. **Wait for deployment** (5-10 minutes)
8. **Your API will be live at**: `https://timecomplexity-analyzer-api.onrender.com`

## Step 2: Update Extension with Render URL

Update your extension to use the Render API:

```bash
# Update background.js
sed -i '' 's/timecomplexityextension-production.up.railway.app/timecomplexity-analyzer-api.onrender.com/g' background.js

# Update manifest.json  
sed -i '' 's/timecomplexityextension-production.up.railway.app/timecomplexity-analyzer-api.onrender.com/g' manifest.json
```

## Step 3: Test the API

```bash
curl https://timecomplexity-analyzer-api.onrender.com/health
```

## Benefits of Render:
✅ **100% Free Forever** - No time limits  
✅ **No Credit Card Required** - Just GitHub signup  
✅ **Automatic Deployments** - Updates when you push to GitHub  
✅ **Custom Domain** - Professional URLs  
✅ **SSL Certificate** - HTTPS included  
✅ **Unlimited Deployments** - Deploy as many times as you want  

## Render Free Tier Limits:
- **750 hours/month** (enough for 24/7 operation)
- **512MB RAM** (plenty for your API)
- **0.1 CPU** (sufficient for your use case)
- **Sleeps after 15 minutes** of inactivity (wakes up on first request)
