@echo off
REM Start script for TimeComplexity Analyzer
cd /d "%~dp0"
call venv\Scripts\activate.bat
cd backend
python main.py
pause
