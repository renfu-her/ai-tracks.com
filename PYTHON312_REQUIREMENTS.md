# Python 3.12 - 專案主要版本

## 為什麼選擇 Python 3.12？

- ✅ **完全支援**：所有依賴套件（Pillow 10.1.0, uWSGI 2.0.23）都完全支援
- ✅ **穩定性**：Python 3.12 是一個成熟穩定的版本
- ✅ **性能優化**：比舊版本有更好的性能表現
- ✅ **相容性**：與所有 Flask 生態系統套件完美相容

## 版本要求

**必須使用 Python 3.12.x**

不支援的版本：
- ❌ Python 3.13（uWSGI 不支援）
- ❌ Python 3.11 或更舊版本（建議使用 3.12）

## 檢查 Python 版本

```bash
# 檢查當前 Python 版本
python --version
# 應該顯示: Python 3.12.x

# 或使用
python3.12 --version
```

## 安裝 Python 3.12

### Windows

1. 從 [Python 官網](https://www.python.org/downloads/) 下載 Python 3.12.x
2. 安裝時勾選 "Add Python to PATH"
3. 驗證安裝：`python --version`

### Linux (Ubuntu/Debian)

```bash
# 添加 deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# 安裝 Python 3.12
sudo apt install python3.12 python3.12-venv python3.12-dev
```

### macOS

```bash
# 使用 Homebrew
brew install python@3.12

# 或使用 pyenv
brew install pyenv
pyenv install 3.12.0
pyenv local 3.12.0
```

## 使用 pyenv 管理 Python 版本

如果你使用 pyenv：

```bash
# 安裝 Python 3.12
pyenv install 3.12.0

# 設定為專案本地版本
cd /path/to/ai-tracks.com
pyenv local 3.12.0

# 驗證
python --version
```

專案已包含 `.python-version` 檔案，pyenv 會自動使用 Python 3.12。

## 虛擬環境設置

```bash
# 明確指定 Python 3.12
python3.12 -m venv venv

# 啟動虛擬環境
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 驗證虛擬環境中的 Python 版本
python --version
```

## 依賴套件版本

專案已針對 Python 3.12 優化：

- **Pillow 10.1.0** - 完全支援 Python 3.12
- **uWSGI 2.0.23** - 完全支援 Python 3.12
- **Flask 3.0.0** - 支援 Python 3.12
- **SQLAlchemy 2.0.23** - 支援 Python 3.12

## 生產環境部署

生產環境應該使用 Python 3.12：

```bash
# 在 Linux 伺服器上
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uwsgi --ini uwsgi.ini
```

## 故障排除

### 問題：找不到 python3.12

**解決方案：**
```bash
# Linux
sudo apt install python3.12

# macOS
brew install python@3.12

# 或使用 pyenv
pyenv install 3.12.0
```

### 問題：虛擬環境使用錯誤的 Python 版本

**解決方案：**
```bash
# 刪除舊的虛擬環境
rm -rf venv

# 使用 Python 3.12 重新創建
python3.12 -m venv venv
source venv/bin/activate
python --version  # 確認是 3.12.x
```

### 問題：套件安裝失敗

**解決方案：**
```bash
# 確保使用 Python 3.12
python --version

# 升級 pip
python -m pip install --upgrade pip setuptools wheel

# 重新安裝依賴
pip install -r requirements.txt
```

## 版本相容性表

| 組件 | Python 3.12 | Python 3.13 | Python 3.11 |
|------|-------------|-------------|-------------|
| Pillow 10.1.0 | ✅ | ⚠️ 需 12.0+ | ✅ |
| uWSGI 2.0.23 | ✅ | ❌ | ✅ |
| Flask 3.0.0 | ✅ | ✅ | ✅ |
| SQLAlchemy 2.0.23 | ✅ | ✅ | ✅ |

## 推薦配置

**開發環境：**
- Python 3.12.x
- Flask 內建伺服器或 Waitress

**生產環境：**
- Python 3.12.x
- Linux/Unix 系統
- uWSGI 2.0.23
- Nginx 反向代理

## 相關檔案

- `.python-version` - pyenv 版本設定
- `runtime.txt` - Heroku 等平台版本設定
- `requirements.txt` - 已針對 Python 3.12 優化

