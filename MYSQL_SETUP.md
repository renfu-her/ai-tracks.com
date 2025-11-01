# MySQL 資料庫設置指南

## 資料庫配置

- **主機**: localhost
- **端口**: 3306 (MySQL 預設)
- **用戶名**: root
- **密碼**: (空)
- **資料庫名稱**: ai-tracks

## 步驟 1: 安裝 MySQL 驅動

```bash
pip install PyMySQL
```

或安裝所有依賴：

```bash
pip install -r requirements.txt
```

## 步驟 2: 創建資料庫

在 MySQL 中創建資料庫：

```sql
-- 登入 MySQL
mysql -u root

-- 創建資料庫
CREATE DATABASE `ai-tracks` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 確認資料庫已創建
SHOW DATABASES;

-- 退出
EXIT;
```

或使用 MySQL Workbench / phpMyAdmin / Laragon 的 MySQL 工具創建資料庫。

## 步驟 3: 配置環境變數

### 方法 1: 使用 .env 檔案（推薦）

1. 複製 `.env.example` 為 `.env`：
```bash
cp .env.example .env
```

2. `.env` 檔案應該包含：
```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/ai-tracks
```

注意：`root:@` 表示用戶名是 root，密碼為空

### 方法 2: 直接修改 config.py

如果不想使用 `.env` 檔案，可以修改 `app/config.py` 中的預設值。

## 步驟 4: 初始化資料庫

```bash
# 啟動虛擬環境（如果還沒啟動）
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 初始化遷移
flask db init

# 創建遷移腳本
flask db migrate -m "Initial migration"

# 應用遷移（創建資料表）
flask db upgrade
```

## 步驟 5: 驗證連接

執行以下命令測試資料庫連接：

```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.engine.connect(); print('MySQL connection successful!')"
```

## 常見問題

### 問題 1: 連接失敗 - Access denied

**解決方案：**
1. 確認 MySQL root 用戶允許從 localhost 連接
2. 檢查 MySQL 服務是否運行
3. 確認密碼是否正確（如果設定過密碼）

```sql
-- 檢查用戶權限
SELECT user, host FROM mysql.user WHERE user='root';

-- 如果需要，創建/更新用戶
CREATE USER 'root'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

### 問題 2: 資料庫不存在

**解決方案：**
```sql
CREATE DATABASE `ai-tracks` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 問題 3: 字符編碼問題

**解決方案：**
確保資料庫使用 utf8mb4 字符集：

```sql
ALTER DATABASE `ai-tracks` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 問題 4: PyMySQL 未安裝

**解決方案：**
```bash
pip install PyMySQL
```

### 問題 5: 連接超時

**解決方案：**
1. 確認 MySQL 服務正在運行
2. 檢查防火牆設置
3. 確認端口 3306 沒有被占用

## Laragon 用戶

如果使用 Laragon，MySQL 應該已經配置好：

1. 啟動 Laragon
2. 點擊 MySQL，打開 phpMyAdmin 或 MySQL 命令行
3. 創建資料庫 `ai-tracks`
4. 使用配置：
   - 主機: localhost
   - 用戶名: root
   - 密碼: (通常是空的，或 Laragon 設定的密碼)

## 資料庫連接字符串格式

MySQL 連接字符串格式：
```
mysql+pymysql://username:password@host:port/database
```

範例：
- 無密碼：`mysql+pymysql://root:@localhost:3306/ai-tracks`
- 有密碼：`mysql+pymysql://root:password@localhost:3306/ai-tracks`
- 不同端口：`mysql+pymysql://root:@localhost:3307/ai-tracks`
- 遠程主機：`mysql+pymysql://root:@192.168.1.100:3306/ai-tracks`

## 驗證設置

執行以下步驟確認設置正確：

```bash
# 1. 檢查 PyMySQL 是否安裝
python -c "import pymysql; print('PyMySQL installed:', pymysql.__version__)"

# 2. 測試資料庫連接
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('Database URI:', app.config['SQLALCHEMY_DATABASE_URI']); db.engine.connect(); print('Connection successful!')"

# 3. 檢查資料表是否創建
flask db upgrade
```

## 備份和還原

### 備份資料庫

```bash
mysqldump -u root -p ai-tracks > backup.sql
```

### 還原資料庫

```bash
mysql -u root -p ai-tracks < backup.sql
```

## 生產環境建議

在生產環境中：

1. **創建專用資料庫用戶**（不要使用 root）：
```sql
CREATE USER 'ai_tracks_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON `ai-tracks`.* TO 'ai_tracks_user'@'localhost';
FLUSH PRIVILEGES;
```

2. **更新 .env 檔案**：
```env
DATABASE_URL=mysql+pymysql://ai_tracks_user:strong_password@localhost:3306/ai-tracks
```

3. **啟用 SSL**（如果可能）：
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'connect_args': {
        'ssl': {'ca': '/path/to/ca-cert.pem'}
    }
}
```

