# Python 3.12 安裝指南

## Python 3.12 環境設置

### 推薦使用 Python 3.12 的原因
- ✅ Pillow 10.1.0 完全支援
- ✅ uWSGI 2.0.23 完全支援
- ✅ 所有依賴套件都有良好支援
- ✅ 穩定性更高

## 安裝步驟

### 1. 確認 Python 版本

```bash
python --version
# 應該顯示: Python 3.12.x
```

### 2. 創建虛擬環境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3.12 -m venv venv
source venv/bin/activate
```

### 3. 升級 pip 和建置工具

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 4. 安裝依賴套件

```bash
pip install -r requirements.txt
```

## Python 3.12 專屬說明

### Pillow 10.1.0
- ✅ 完全支援 Python 3.12
- ✅ 無需額外建置工具
- ✅ 預編譯 wheel 可用

### uWSGI 2.0.23
- ✅ 完全支援 Python 3.12
- ✅ Linux/Unix 系統可用
- ⚠️ Windows 上需使用替代方案（見下方）

## Windows 開發環境

在 Windows 上開發時，uWSGI 可能無法安裝。可以使用以下替代方案：

### 選項 1: 使用 Flask 內建伺服器（開發用）

```bash
python run.py
```

### 選項 2: 使用 Waitress（Windows 相容的 WSGI 伺服器）

```bash
pip install waitress
```

然後修改 `run.py`：

```python
from waitress import serve
from app import create_app

app = create_app()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
```

### 選項 3: 使用 WSL（Windows Subsystem for Linux）

在 WSL 中運行 uWSGI：

```bash
# 在 WSL 中
pip install uwsgi
uwsgi --ini uwsgi.ini
```

## 生產環境部署

生產環境建議使用 Linux 伺服器 + Python 3.12 + uWSGI：

```bash
# 在 Linux 伺服器上
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uwsgi --ini uwsgi.ini
```

## 版本相容性表

| 套件 | Python 3.12 | Python 3.13 |
|------|-------------|-------------|
| Pillow 10.1.0 | ✅ | ⚠️ 需 12.0+ |
| uWSGI 2.0.23 | ✅ | ❌ 不支援 |
| Flask 3.0.0 | ✅ | ✅ |
| SQLAlchemy 2.0.23 | ✅ | ✅ |

## 故障排除

### 問題：Pillow 安裝失敗

解決方案：
```bash
pip install --upgrade pip setuptools wheel
pip install Pillow==10.1.0
```

### 問題：uWSGI 在 Windows 無法安裝

解決方案：
- 使用 `python run.py` 開發
- 或使用 Waitress：`pip install waitress`
- 或使用 WSL

### 問題：缺少建置工具

解決方案：
```bash
# Windows
pip install --upgrade pip setuptools wheel

# Linux
sudo apt-get install python3-dev build-essential
```

## 推薦配置

**開發環境：**
- Python 3.12.x
- Flask 內建伺服器或 Waitress

**生產環境：**
- Python 3.12.x
- Linux/Unix 系統
- uWSGI 2.0.23
- Nginx 反向代理

