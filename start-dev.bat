@echo off
REM 啟動開發伺服器（使用 Python 3.12）

REM 設定 Python 3.12 路徑（請根據你的安裝位置修改）
set PYTHON312_PATH=C:\Python312
set PYTHON312_ALT=C:\Program Files\Python312
set PYTHON312_ALT2=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312
set PYTHON312_LARAGON=D:\laragon\bin\python\python-3.12

REM 尋找並設定 Python 3.12 到 PATH
if exist "%PYTHON312_LARAGON%\python.exe" (
    set PATH=%PYTHON312_LARAGON%;%PYTHON312_LARAGON%\Scripts;%PATH%
) else if exist "%PYTHON312_PATH%\python.exe" (
    set PATH=%PYTHON312_PATH%;%PYTHON312_PATH%\Scripts;%PATH%
) else if exist "%PYTHON312_ALT%\python.exe" (
    set PATH=%PYTHON312_ALT%;%PYTHON312_ALT%\Scripts;%PATH%
) else if exist "%PYTHON312_ALT2%\python.exe" (
    set PATH=%PYTHON312_ALT2%;%PYTHON312_ALT2%\Scripts;%PATH%
)

REM 檢查虛擬環境是否存在
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run setup-python312.bat first.
    pause
    exit /b 1
)

REM 啟動虛擬環境
call venv\Scripts\activate.bat

REM 顯示 Python 版本
echo Python version:
python --version
echo.

REM 啟動 Flask 開發伺服器
echo Starting development server...
echo.
python run.py

