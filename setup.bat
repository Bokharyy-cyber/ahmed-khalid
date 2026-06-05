@echo off
REM BOKHARY - Setup Script for Windows
REM هذا السكريبت يقوم بإعداد المشروع بشكل سريع على Windows

echo.
echo 🛡️ BOKHARY - Security Setup Script (Windows)
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed! Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found:
python --version
echo.

REM Go to backend directory
cd backend
if errorlevel 1 (
    echo ❌ Error: Could not find backend directory
    pause
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv
call venv\Scripts\activate
echo ✅ Virtual environment created
echo.

REM Install requirements
echo 📚 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error installing dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed
echo.

REM Create .env file
if not exist .env (
    echo ⚙️ Creating .env file...
    copy env.example .env
    
    echo.
    echo ⚠️  IMPORTANT: Edit .env file with your settings:
    echo.
    echo    Open .env with Notepad and fill in:
    echo.
    echo    Required fields:
    echo    - ADMIN_API_KEY (run: python -c "import secrets; print(secrets.token_urlsafe(32))")
    echo    - OWNER_EMAIL (your actual email)
    echo    - GMAIL_USER (your gmail)
    echo    - GMAIL_APP_PASSWORD (from myaccount.google.com/apppasswords)
    echo.
) else (
    echo ✅ .env file already exists (skipped)
)

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your actual values
echo 2. Run: python -m uvicorn main:app --reload
echo 3. Open: http://localhost:8000
echo.
pause
