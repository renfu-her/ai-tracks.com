@echo off
REM 專案專用 Python 3.12 設定腳本
REM 此腳本會設定 Python 3.12 並創建虛擬環境

echo ======================================
echo AI Tracks - Python 3.12 Setup
echo ======================================
echo.

REM 設定 Python 3.12 路徑（請根據你的安裝位置修改）
set PYTHON312_PATH=C:\Python312
set PYTHON312_ALT=C:\Program Files\Python312
set PYTHON312_ALT2=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312
set PYTHON312_LARAGON=D:\laragon\bin\python\python-3.12

REM 尋找 Python 3.12
set PYTHON_CMD=
if exist "%PYTHON312_LARAGON%\python.exe" (
    set PYTHON_CMD=%PYTHON312_LARAGON%\python.exe
    echo Found Python 3.12 at: %PYTHON312_LARAGON%
) else if exist "%PYTHON312_PATH%\python.exe" (
    set PYTHON_CMD=%PYTHON312_PATH%\python.exe
    echo Found Python 3.12 at: %PYTHON312_PATH%
) else if exist "%PYTHON312_ALT%\python.exe" (
    set PYTHON_CMD=%PYTHON312_ALT%\python.exe
    echo Found Python 3.12 at: %PYTHON312_ALT%
) else if exist "%PYTHON312_ALT2%\python.exe" (
    set PYTHON_CMD=%PYTHON312_ALT2%\python.exe
    echo Found Python 3.12 at: %PYTHON312_ALT2%
) else (
    REM 嘗試使用 py launcher
    py -3.12 --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=py -3.12
        echo Found Python 3.12 via py launcher
    ) else (
        echo ERROR: Python 3.12 not found!
        echo.
        echo Please install Python 3.12 from:
        echo https://www.python.org/downloads/release/python-3120/
        echo.
        echo Or update PYTHON312_PATH in this script to point to your Python 3.12 installation.
        pause
        exit /b 1
    )
)

REM 顯示 Python 版本
echo.
echo Checking Python version...
%PYTHON_CMD% --version
if %errorlevel% neq 0 (
    echo ERROR: Failed to run Python 3.12
    pause
    exit /b 1
)

REM 設定 PATH（臨時，僅此終端會話）
set PATH=%PYTHON312_PATH%;%PYTHON312_PATH%\Scripts;%PATH%

REM 創建虛擬環境
echo.
echo Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists.
    echo To recreate, delete the venv folder first.
) else (
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)

REM 啟動虛擬環境
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM 驗證虛擬環境中的 Python 版本
echo.
echo Verifying Python version in virtual environment...
python --version

REM 升級 pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM 安裝依賴
echo.
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo WARNING: Some packages failed to install
    echo You may need to install them manually
)

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo To start the development server, run:
echo   start-dev.bat
echo.
echo Or manually:
echo   venv\Scripts\activate
echo   python run.py
echo.
pause

