# 後端管理系統設置完成

## 已完成的功能

### 1. 用戶認證系統
- ✅ User 模型（包含 role: admin/user）
- ✅ Flask-Login 整合
- ✅ 登入/登出功能
- ✅ 權限控制（admin_required 裝飾器）

### 2. 後端路由
- ✅ `/backend/login` - 登入頁面
- ✅ `/backend/logout` - 登出
- ✅ `/backend/dashboard` - 儀表板（需要 admin）
- ✅ `/backend/users` - 用戶管理（需要 admin）

### 3. 資料庫
- ✅ users 表已創建
- ✅ 預設 admin 用戶已創建

## 預設登入資訊

**首次登入：**
- 用戶名：`admin`
- 密碼：`admin123`
- 角色：`admin`

⚠️ **重要：登入後請立即修改密碼！**

## 使用方式

### 1. 安裝 Flask-Login

```bash
pip install Flask-Login==0.6.3
```

或安裝所有依賴：

```bash
pip install -r requirements.txt
```

### 2. 訪問後台

啟動應用程式後，訪問：

```
http://localhost:5000/backend/login
```

### 3. 登入後台

使用預設帳號登入：
- 用戶名：`admin`
- 密碼：`admin123`

### 4. 用戶管理

登入後，在「用戶管理」頁面可以：
- 查看所有用戶
- 新增用戶
- 啟用/停用用戶
- 刪除用戶（無法刪除自己）

## 權限說明

### Admin 角色
- ✅ 可以訪問所有後台功能
- ✅ 可以管理用戶（新增、刪除、啟用/停用）
- ✅ 可以查看儀表板統計資訊

### User 角色
- ❌ 無法訪問後台管理功能
- ⚠️ 目前僅 admin 可以訪問後台

## 路由保護

所有後台路由都受到保護：

- **未登入用戶**：會被重定向到 `/backend/login`
- **一般用戶**：會被拒絕訪問（403 錯誤）
- **管理員**：可以正常訪問

## 創建新用戶

### 方法 1: 透過後台界面

1. 登入後台
2. 點擊「用戶管理」
3. 點擊「新增用戶」
4. 填寫表單並提交

### 方法 2: 使用 Python 腳本

```python
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    user = User(
        username='newuser',
        email='user@example.com',
        role='user'  # 或 'admin'
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
```

## 資料庫結構

users 表包含以下欄位：
- `id` - 主鍵
- `username` - 用戶名（唯一）
- `email` - 電子郵件（唯一）
- `password_hash` - 密碼雜湊
- `role` - 角色（admin/user）
- `is_active` - 是否啟用
- `created_at` - 建立時間
- `updated_at` - 更新時間
- `last_login` - 最後登入時間

## 安全建議

1. **修改預設密碼**：首次登入後立即修改
2. **使用強密碼**：至少 8 個字元，包含大小寫字母、數字和特殊字符
3. **定期更新密碼**：建議每 3-6 個月更新一次
4. **限制管理員數量**：僅授予必要人員管理員權限
5. **啟用 HTTPS**：生產環境必須使用 HTTPS

## 故障排除

### 問題：無法登入

**解決方案：**
1. 確認用戶名和密碼正確
2. 確認用戶帳號是啟用狀態（is_active=True）
3. 檢查資料庫連接是否正常

### 問題：權限不足

**解決方案：**
1. 確認用戶角色是 'admin'
2. 檢查路由是否正確使用 @admin_required 裝飾器

### 問題：忘記密碼

**解決方案：**
```python
# 重置 admin 密碼
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='admin').first()
    if user:
        user.set_password('new_password')
        db.session.commit()
        print("Password reset successfully!")
```

## 下一步

後端管理系統已建立完成，你可以：

1. 訪問後台：`http://localhost:5000/backend/login`
2. 管理用戶：在用戶管理頁面新增、編輯、刪除用戶
3. 擴展功能：可以添加更多管理功能（案例管理、消息管理等）

