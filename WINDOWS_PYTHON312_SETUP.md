# Windows 上設定 Python 3.12 為主版本

## 方法 1: 安裝 Python 3.12 並設定為系統默認（推薦）

### 步驟 1: 下載並安裝 Python 3.12

1. 訪問 [Python 官方網站](https://www.python.org/downloads/release/python-3120/)
2. 下載 **Windows installer (64-bit)** 或 **Windows installer (32-bit)**
3. 執行安裝程式
4. **重要：勾選 "Add Python 3.12 to PATH"**
5. 選擇 "Install Now" 或 "Customize installation"

### 步驟 2: 調整 PATH 順序

安裝後，Python 3.12 會自動添加到 PATH。如果系統有 Python 3.13，需要調整順序：

1. 開啟「系統環境變數」
   - 按 `Win + R`，輸入 `sysdm.cpl`，按 Enter
   - 點擊「進階」→「環境變數」
   
2. 編輯 PATH 變數
   - 在「系統變數」中找到 `Path`
   - 編輯 PATH
   - 將 Python 3.12 的路徑移到 Python 3.13 之前
   - 例如：
     ```
     C:\Python312\
     C:\Python312\Scripts\
     C:\Python313\        (移到後面)
     C:\Python313\Scripts\
     ```

3. 重新啟動終端機

### 步驟 3: 驗證

```bash
python --version
# 應該顯示: Python 3.12.x

python -m pip --version
# 確認 pip 也是 Python 3.12 的
```

## 方法 2: 使用 Python Launcher (py launcher)

### 步驟 1: 安裝 Python 3.12（同上）

### 步驟 2: 設定專案使用 Python 3.12

創建 `py.ini` 檔案（如果不存在）：
- 位置：`%LOCALAPPDATA%\py.ini` 或 `%APPDATA%\py.ini`

內容：
```ini
[defaults]
python=3.12
```

### 步驟 3: 在專案中使用

```bash
# 使用 Python 3.12
py -3.12 --version

# 創建虛擬環境
py -3.12 -m venv venv

# 啟動虛擬環境
venv\Scripts\activate

# 驗證
python --version  # 應該是 3.12.x
```

## 方法 3: 只在此專案中使用 Python 3.12（不改變系統設置）

### 步驟 1: 下載 Python 3.12

下載 [Python 3.12 可攜式版本](https://www.python.org/downloads/release/python-3120/)
或安裝到特定目錄（如 `C:\Python312\`）

### 步驟 2: 修改專案的 setup.bat

創建一個專案專用的啟動腳本：

```batch
@echo off
REM 專案專用 Python 3.12 設定

REM 設定 Python 3.12 路徑（根據你的安裝位置修改）
set PYTHON312_PATH=C:\Python312
set PATH=%PYTHON312_PATH%;%PYTHON312_PATH%\Scripts;%PATH%

REM 顯示 Python 版本
python --version

REM 創建虛擬環境（如果不存在）
if not exist "venv" (
    echo Creating virtual environment with Python 3.12...
    python -m venv venv
)

REM 啟動虛擬環境
call venv\Scripts\activate.bat

REM 顯示虛擬環境中的 Python 版本
python --version

REM 安裝依賴
if not exist "venv\Lib\site-packages\flask" (
    echo Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
)

echo.
echo Python 3.12 environment ready!
echo.
```

### 步驟 3: 創建專案啟動腳本

創建 `start-dev.bat`：

```batch
@echo off
REM 啟動開發伺服器

REM 設定 Python 3.12 路徑
set PYTHON312_PATH=C:\Python312
set PATH=%PYTHON312_PATH%;%PYTHON312_PATH%\Scripts;%PATH%

REM 啟動虛擬環境
call venv\Scripts\activate.bat

REM 啟動 Flask 開發伺服器
python run.py
```

## 方法 4: 使用 conda/miniconda（推薦給開發者）

### 步驟 1: 安裝 Miniconda

下載並安裝 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### 步驟 2: 創建 Python 3.12 環境

```bash
# 創建專案環境
conda create -n ai-tracks python=3.12 -y

# 啟動環境
conda activate ai-tracks

# 驗證版本
python --version  # 應該是 Python 3.12.x

# 安裝依賴
pip install -r requirements.txt
```

### 步驟 3: 每次使用時啟動環境

```bash
conda activate ai-tracks
python run.py
```

## 快速解決方案：創建專案專用啟動腳本

我已經為你創建了一個專案專用的啟動腳本：

### 使用方式：

1. 安裝 Python 3.12 到 `C:\Python312\`（或修改腳本中的路徑）
2. 執行 `setup-python312.bat`（會自動設定並創建虛擬環境）
3. 之後使用 `start-dev.bat` 啟動開發伺服器

### 驗證是否成功：

```bash
# 執行後應該看到
Python 3.12.x
```

## 推薦方案

**對於開發環境：**
- 使用 **方法 4 (conda)** - 最乾淨，不會影響系統 Python
- 或 **方法 3** - 專案專用，不改變系統設置

**對於生產環境：**
- 使用 **方法 1** - 直接設定系統默認版本

## 疑難排解

### 問題：安裝後仍顯示 Python 3.13

**解決方案：**
1. 檢查 PATH 順序
2. 重新啟動終端機/命令提示字元
3. 確認 Python 3.12 已正確安裝：`where python`

### 問題：多個 Python 版本衝突

**解決方案：**
- 使用 `py -3.12` 明確指定版本
- 或使用 conda 環境隔離

### 問題：虛擬環境仍使用錯誤版本

**解決方案：**
```bash
# 刪除舊的虛擬環境
rmdir /s venv

# 使用 Python 3.12 重新創建
py -3.12 -m venv venv
# 或
C:\Python312\python.exe -m venv venv
```

