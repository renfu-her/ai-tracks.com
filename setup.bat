@echo off
REM Setup script for AI Tracks Flask Application (Windows)

echo ======================================
echo AI Tracks - Flask Setup Script
echo ======================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    echo Note: This project requires Python 3.12
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo .env file created
    echo Please review and update .env file with your configuration
) else (
    echo .env file already exists
)

REM Create upload directories
echo.
echo Creating upload directories...
if not exist "uploads\cases" mkdir uploads\cases
if not exist "uploads\news" mkdir uploads\news
if not exist "uploads\sliders" mkdir uploads\sliders
echo Upload directories created

REM Initialize database
echo.
echo Initializing database...

if not exist "migrations" (
    echo Initializing Flask-Migrate...
    flask db init
)

echo Creating migration...
flask db migrate -m "Initial migration"

echo Applying migration...
flask db upgrade

echo Database initialized

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo To run the development server:
echo   venv\Scripts\activate
echo   python run.py
echo.
echo To run with uWSGI (production):
echo   1. Update uwsgi.ini with your paths
echo   2. uwsgi --ini uwsgi.ini
echo.
echo The application will be available at:
echo   http://localhost:5000
echo.

pause

