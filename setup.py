#!/usr/bin/env python3
"""
Setup script for TimeComplexity Analyzer
Automates the installation and configuration process
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class SetupManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.venv_dir = self.project_root / "venv"
        
    def print_banner(self):
        """Print setup banner"""
        print("⏱️  TimeComplexity Analyzer Setup")
        print("=" * 50)
        print("Setting up Chrome extension with Python backend")
        print()
    
    def check_python_version(self):
        """Check Python version compatibility"""
        print("🐍 Checking Python version...")
        if sys.version_info < (3, 8):
            print(f"❌ Error: Python 3.8+ required, found {sys.version}")
            sys.exit(1)
        print(f"✅ Python {sys.version.split()[0]} detected")
    
    def create_virtual_environment(self):
        """Create virtual environment"""
        print("\n📦 Creating virtual environment...")
        if self.venv_dir.exists():
            print("✅ Virtual environment already exists")
            return
        
        try:
            subprocess.check_call([sys.executable, "-m", "venv", str(self.venv_dir)])
            print("✅ Virtual environment created successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating virtual environment: {e}")
            sys.exit(1)
    
    def get_venv_python(self):
        """Get path to virtual environment Python"""
        if platform.system() == "Windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("\n📦 Installing dependencies...")
        venv_python = self.get_venv_python()
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("❌ Error: requirements.txt not found")
            sys.exit(1)
        
        try:
            subprocess.check_call([str(venv_python), "-m", "pip", "install", "-r", str(requirements_file)])
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            sys.exit(1)
    
    def create_icons_placeholder(self):
        """Create placeholder icons if they don't exist"""
        print("\n🎨 Checking icons...")
        icons_dir = self.project_root / "icons"
        
        if not icons_dir.exists():
            icons_dir.mkdir()
            print("✅ Created icons directory")
        
        # Check if icons exist
        required_icons = ["icon16.png", "icon48.png", "icon128.png"]
        missing_icons = []
        
        for icon in required_icons:
            if not (icons_dir / icon).exists():
                missing_icons.append(icon)
        
        if missing_icons:
            print(f"⚠️  Missing icons: {', '.join(missing_icons)}")
            print("   Please add icon files to the icons/ directory")
            print("   See icons/README.md for instructions")
        else:
            print("✅ All icons found")
    
    def test_backend(self):
        """Test the backend server"""
        print("\n🧪 Testing backend...")
        venv_python = self.get_venv_python()
        
        try:
            # Test import
            result = subprocess.run(
                [str(venv_python), "-c", "from backend.analyzer import TimeComplexityAnalyzer; print('✅ Backend imports successfully')"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                print(result.stdout.strip())
            else:
                print("❌ Backend test failed")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error testing backend: {e}")
    
    def create_start_scripts(self):
        """Create convenient start scripts"""
        print("\n📝 Creating start scripts...")
        
        # Create start script for Unix-like systems
        if platform.system() != "Windows":
            start_script = self.project_root / "start.sh"
            with open(start_script, 'w') as f:
                f.write("""#!/bin/bash
# Start script for TimeComplexity Analyzer
cd "$(dirname "$0")"
source venv/bin/activate
cd backend
python main.py
""")
            os.chmod(start_script, 0o755)
            print("✅ Created start.sh")
        
        # Create start script for Windows
        start_script_win = self.project_root / "start.bat"
        with open(start_script_win, 'w') as f:
            f.write("""@echo off
REM Start script for TimeComplexity Analyzer
cd /d "%~dp0"
call venv\\Scripts\\activate.bat
cd backend
python main.py
pause
""")
        print("✅ Created start.bat")
    
    def print_next_steps(self):
        """Print next steps for the user"""
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Start the backend server:")
        if platform.system() == "Windows":
            print("   Double-click start.bat or run: python start_server.py")
        else:
            print("   Run: ./start.sh or python start_server.py")
        
        print("\n2. Load the Chrome extension:")
        print("   - Open Chrome and go to chrome://extensions/")
        print("   - Enable 'Developer mode'")
        print("   - Click 'Load unpacked' and select this directory")
        
        print("\n3. Test the extension:")
        print("   - Click the extension icon in Chrome toolbar")
        print("   - Try analyzing some code")
        print("   - Visit a coding platform to test auto-extraction")
        
        print("\n📖 For more information, see README.md")
        print("\n🔧 Troubleshooting:")
        print("   - If backend fails to start, check that port 8000 is available")
        print("   - If extension doesn't work, reload it in chrome://extensions/")
        print("   - Check the console for error messages")
    
    def run_setup(self):
        """Run the complete setup process"""
        self.print_banner()
        self.check_python_version()
        self.create_virtual_environment()
        self.install_dependencies()
        self.create_icons_placeholder()
        self.test_backend()
        self.create_start_scripts()
        self.print_next_steps()

def main():
    """Main function"""
    setup = SetupManager()
    setup.run_setup()

if __name__ == "__main__":
    main() 