#!/usr/bin/env python3
"""
Start script for TimeComplexity Analyzer backend server
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_venv():
    """Check if virtual environment is activated"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
        return True
    else:
        print("⚠️  Warning: Virtual environment not detected")
        print("   Consider activating it: source venv/bin/activate")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting TimeComplexity Analyzer server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API documentation: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Start the server
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except FileNotFoundError:
        print("❌ Error: backend/main.py not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("⏱️  TimeComplexity Analyzer Backend Server")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check virtual environment
    check_venv()
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ Error: requirements.txt not found")
        sys.exit(1)
    
    # Check if backend directory exists
    if not os.path.exists("backend"):
        print("❌ Error: backend directory not found")
        sys.exit(1)
    
    # Install dependencies if needed
    try:
        import fastapi
        print("✅ FastAPI is already installed")
    except ImportError:
        print("📦 FastAPI not found, installing dependencies...")
        install_dependencies()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main() 