# 🆓 Deploy to PythonAnywhere (100% Free Forever)

PythonAnywhere offers free hosting specifically for Python apps.

## Step 1: Sign Up for PythonAnywhere

1. **Go to**: https://www.pythonanywhere.com
2. **Sign up** for free account (no credit card needed)
3. **Verify your email**

## Step 2: Upload Your Code

1. **Go to "Files"** tab
2. **Create a new directory**: `timecomplexity-analyzer`
3. **Upload your files**:
   - `backend/` folder
   - `requirements.txt`
   - `Procfile`

## Step 3: Install Dependencies

1. **Go to "Consoles"** tab
2. **Open a Bash console**
3. **Run**:
   ```bash
   cd timecomplexity-analyzer
   pip3.10 install --user -r requirements.txt
   ```

## Step 4: Create Web App

1. **Go to "Web"** tab
2. **Click "Add a new web app"**
3. **Choose "Manual configuration"**
4. **Select Python 3.10**
5. **Configure**:
   - **Source code**: `/home/yourusername/timecomplexity-analyzer`
   - **Working directory**: `/home/yourusername/timecomplexity-analyzer`
   - **WSGI file**: `backend/main.py`

## Step 5: Configure WSGI

Edit the WSGI file:
```python
import sys
path = '/home/yourusername/timecomplexity-analyzer'
if path not in sys.path:
    sys.path.append(path)

from backend.main import app
application = app
```

## Benefits of PythonAnywhere:
✅ **100% Free Forever** - No time limits  
✅ **No Credit Card Required** - Just email signup  
✅ **Python-focused** - Perfect for Python APIs  
✅ **Easy setup** - Web interface  
✅ **Custom domains** - Professional URLs  
✅ **SSL included** - HTTPS support  

## PythonAnywhere Free Tier:
- **1 web app**
- **512MB disk space**
- **100 seconds CPU time/day**
- **Custom domain support**
