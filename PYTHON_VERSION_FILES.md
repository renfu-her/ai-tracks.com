# Python Version Configuration Files

這個專案已設定為使用 **Python 3.12** 作為主要版本。

## 檔案說明

### `.python-version`
- 用於 pyenv 自動切換 Python 版本
- 內容：`3.12`
- 如果使用 pyenv，進入專案目錄時會自動切換到 Python 3.12

### `runtime.txt`
- 用於 Heroku、Railway、Render 等平台部署
- 內容：`python-3.12.0`
- 告訴平台使用 Python 3.12.0

### `requirements.txt`
- 已針對 Python 3.12 優化所有依賴版本
- Pillow 10.1.0 - 完全支援 Python 3.12
- uWSGI 2.0.23 - 完全支援 Python 3.12

## 使用方式

### 使用 pyenv

```bash
# 如果還沒有安裝 Python 3.12
pyenv install 3.12.0

# 進入專案目錄，pyenv 會自動使用 3.12
cd /path/to/ai-tracks.com
python --version  # 會顯示 Python 3.12.x
```

### 不使用 pyenv

```bash
# 明確指定 Python 3.12
python3.12 -m venv venv
source venv/bin/activate
python --version  # 確認是 3.12.x
```

### 在 CI/CD 中使用

這些檔案會自動被以下平台識別：
- Heroku（使用 runtime.txt）
- Railway（使用 runtime.txt）
- Render（使用 runtime.txt）
- GitHub Actions（使用 .python-version）

## 驗證

```bash
# 檢查當前 Python 版本
python --version
# 應該顯示: Python 3.12.x

# 在虛擬環境中檢查
source venv/bin/activate
python --version
```

