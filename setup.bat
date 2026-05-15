@echo off
title 🦈 WAR PHISH Installer
color 0A

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                 🦈 WAR PHISH INSTALLATION                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [1/5] Checking Python version...
py -3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Python 3.7+ not found. Please install Python from python.org
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('py -3 --version 2^>^&1') do set PY_VER=%%i
echo ✓ Python %PY_VER% detected

echo.
echo [2/5] Creating virtual environment...
py -3 -m venv venv
call venv\Scripts\activate.bat

echo.
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo [4/5] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [5/5] Creating directories...
mkdir .warphish 2>nul
mkdir reports 2>nul
mkdir logs 2>nul
mkdir phishing_pages 2>nul
mkdir wordlists 2>nul
mkdir captured_credentials 2>nul

if not exist .env copy .env.example .env

echo.
echo ════════════════════════════════════════════════════════════════
echo                     ✅ INSTALLATION COMPLETE!                    
echo ════════════════════════════════════════════════════════════════
echo.
echo Next steps:
echo   1. Edit .env file with your bot tokens
echo   2. Run: venv\Scripts\activate
echo   3. Run: python warphish.py
echo   4. Access web dashboard: http://localhost:5000
echo.
echo ⚠️  Run as Administrator for full functionality
pause