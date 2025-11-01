# Laragon 中使用 Python 3.12 的設置指南

## 你的當前環境

- Laragon 安裝位置：`D:\laragon\`
- 當前 Python：`D:\laragon\bin\python\python-3.13\python.exe`
- 需要：Python 3.12

## 方法 1: 在 Laragon 中安裝 Python 3.12（推薦）

### 步驟 1: 下載 Python 3.12

1. 訪問 [Python 3.12.0 下載頁面](https://www.python.org/downloads/release/python-3120/)
2. 下載 **Windows installer (64-bit)**
3. 執行安裝程式

### 步驟 2: 安裝到 Laragon 目錄

**選項 A：手動安裝到 Laragon**

1. 執行 Python 3.12 安裝程式
2. 選擇 "Customize installation"
3. 將安裝路徑改為：`D:\laragon\bin\python\python-3.12\`
4. 完成安裝

**選項 B：安裝到系統，然後複製到 Laragon**

1. 安裝 Python 3.12 到系統（例如 `C:\Python312\`）
2. 複製整個資料夾到：`D:\laragon\bin\python\python-3.12\`

### 步驟 3: 驗證安裝

```bash
D:\laragon\bin\python\python-3.12\python.exe --version
# 應該顯示: Python 3.12.x
```

### 步驟 4: 更新專案腳本

修改 `setup-python312.bat`，將路徑改為：

```batch
set PYTHON312_PATH=D:\laragon\bin\python\python-3.12
```

## 方法 2: 使用專案專用腳本（不需要改變 Laragon）

我已經為你創建了專用腳本，會自動尋找 Python 3.12。

### 使用步驟：

1. **安裝 Python 3.12**（如果還沒安裝）
   - 下載：https://www.python.org/downloads/release/python-3120/
   - 安裝到任意位置（例如 `C:\Python312\`）

2. **執行專案設置腳本**
   ```bash
   setup-python312.bat
   ```
   
   腳本會自動：
   - 尋找 Python 3.12
   - 創建虛擬環境
   - 安裝所有依賴

3. **啟動開發伺服器**
   ```bash
   start-dev.bat
   ```

### 修改腳本中的路徑（如果需要）

如果 Python 3.12 安裝在不同的位置，編輯 `setup-python312.bat`：

```batch
REM 修改這一行，指向你的 Python 3.12 安裝位置
set PYTHON312_PATH=C:\Python312
```

## 方法 3: 使用 py launcher（最簡單）

如果已安裝 Python 3.12，可以直接使用：

```bash
# 檢查 Python 3.12 是否可用
py -3.12 --version

# 如果可用，創建虛擬環境
py -3.12 -m venv venv

# 啟動虛擬環境
venv\Scripts\activate

# 驗證版本
python --version  # 應該是 3.12.x

# 安裝依賴
pip install -r requirements.txt
```

## 快速開始（推薦）

### 步驟 1: 安裝 Python 3.12

如果還沒安裝：
1. 下載：https://www.python.org/downloads/release/python-3120/
2. 安裝時勾選 "Add Python to PATH"

### 步驟 2: 執行專案設置

```bash
# 執行設置腳本（會自動尋找 Python 3.12）
setup-python312.bat
```

### 步驟 3: 啟動開發伺服器

```bash
start-dev.bat
```

## 驗證

執行後應該看到：

```bash
Python 3.12.x
Flask development server running on http://localhost:5000
```

## 疑難排解

### 問題：找不到 Python 3.12

**解決方案：**
1. 確認 Python 3.12 已安裝
2. 編輯 `setup-python312.bat`，修改 `PYTHON312_PATH` 為實際安裝路徑
3. 或使用 `py -3.12` 命令

### 問題：虛擬環境仍使用 Python 3.13

**解決方案：**
```bash
# 刪除舊的虛擬環境
rmdir /s venv

# 使用 Python 3.12 重新創建
D:\laragon\bin\python\python-3.12\python.exe -m venv venv
# 或
py -3.12 -m venv venv
```

### 問題：PATH 衝突

**解決方案：**
使用專案專用腳本（`setup-python312.bat`），它會臨時設定 PATH，不會影響系統設置。

## 推薦配置

**開發環境：**
- 安裝 Python 3.12 到系統
- 使用 `setup-python312.bat` 設置專案
- 使用 `start-dev.bat` 啟動開發伺服器

**優點：**
- ✅ 不影響 Laragon 的 Python 3.13
- ✅ 專案使用專屬的 Python 3.12 環境
- ✅ 可以同時運行多個專案（不同 Python 版本）

