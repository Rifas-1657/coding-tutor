@echo off
echo Starting Coding Tutor Backend Server...
echo.
echo Make sure you have:
echo 1. Python 3.8+ installed
echo 2. All dependencies installed (pip install -r requirements.txt)
echo 3. Docker Desktop running (for code execution)
echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
python main.py
