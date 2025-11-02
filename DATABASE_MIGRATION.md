# 数据库迁移指南

## 问题描述

错误信息：
```
Table 'blog.project_cases' doesn't exist
```

这表示数据库表尚未创建，需要运行数据库迁移。

## 快速修复步骤

### 在服务器上执行：

```bash
cd /home/ai-tracks-blog/htdocs/blog.ai-tracks.com

# 激活虚拟环境
source .venv/bin/activate

# 运行迁移脚本
bash run_migrations.sh
```

### 或手动执行：

```bash
cd /home/ai-tracks-blog/htdocs/blog.ai-tracks.com
source .venv/bin/activate

# 1. 测试数据库连接
python -c "
from app import create_app, db
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    db.engine.connect()
    print('数据库连接成功')
"

# 2. 检查迁移状态
flask db current

# 3. 如果有新的模型变更，创建迁移
flask db migrate -m "Update schema"

# 4. 应用迁移（创建所有表）
flask db upgrade

# 5. 验证表是否创建
python -c "
from app import create_app, db
from app.models import ProjectCase
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    # 尝试查询，如果表不存在会报错
    ProjectCase.query.first()
    print('project_cases 表已创建')
"
```

## 检查数据库配置

确保 `.env` 文件中的数据库配置正确：

```bash
# 查看当前数据库配置
cd /home/ai-tracks-blog/htdocs/blog.ai-tracks.com
source .venv/bin/activate

python -c "
import os
from dotenv import load_dotenv
load_dotenv()

print('DATABASE_URL:', os.getenv('DATABASE_URL'))
print('DB_HOST:', os.getenv('DB_HOST'))
print('DB_PORT:', os.getenv('DB_PORT'))
print('DB_USER:', os.getenv('DB_USER'))
print('DB_NAME:', os.getenv('DB_NAME'))
"
```

## 常见问题

### 问题 1: 数据库不存在

**错误**: `Unknown database 'xxx'`

**解决方案**:
```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE `blog` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# 或使用你的数据库名称
CREATE DATABASE `ai-tracks` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出
EXIT;
```

### 问题 2: 权限不足

**错误**: `Access denied` 或 `Permission denied`

**解决方案**:
```sql
-- 登录 MySQL
mysql -u root -p

-- 授予权限
GRANT ALL PRIVILEGES ON `blog`.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;

-- 或授予所有权限
GRANT ALL PRIVILEGES ON *.* TO 'your_user'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

### 问题 3: 迁移失败

**解决方案**:
```bash
# 检查迁移历史
flask db history

# 查看当前版本
flask db current

# 如果需要，可以降级然后重新升级
flask db downgrade
flask db upgrade

# 或者重置迁移（谨慎使用）
# rm -rf migrations/
# flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade
```

### 问题 4: 数据库名称不匹配

如果错误显示数据库是 `blog`，但你的配置是其他名称：

**解决方案**:
1. 检查 `.env` 文件中的 `DB_NAME` 或 `DATABASE_URL`
2. 确保数据库名称一致
3. 如果需要，创建正确的数据库：
```sql
CREATE DATABASE `blog` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 验证迁移成功

运行以下命令验证所有表都已创建：

```bash
python -c "
from app import create_app, db
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print('数据库中的表:')
    for table in tables:
        print('  -', table)
"
```

应该看到以下表：
- `project_cases`
- `case_photos`
- `news`
- `product_categories`
- `users`
- `contacts`
- `page_settings`
- `sliders`
- `alembic_version` (迁移版本表)

## 完整的迁移流程

```bash
# 1. 进入项目目录
cd /home/ai-tracks-blog/htdocs/blog.ai-tracks.com

# 2. 激活虚拟环境
source .venv/bin/activate

# 3. 检查数据库配置
cat .env | grep -E "DB_|DATABASE_URL"

# 4. 测试数据库连接
python -c "
from app import create_app, db
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    db.engine.connect()
    print('连接成功')
"

# 5. 运行迁移
flask db upgrade

# 6. 验证表
python -c "
from app import create_app, db
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print('表数量:', len(tables))
    print('表列表:', ', '.join(tables))
"

# 7. 重启应用
sudo systemctl restart uwsgi
# 或
sudo systemctl restart uwsgi-ai-tracks
```

## 注意事项

1. **备份数据库**: 在生产环境运行迁移前，建议先备份数据库
2. **测试环境**: 先在测试环境验证迁移脚本
3. **权限**: 确保数据库用户有创建表、修改表结构的权限
4. **日志**: 查看应用日志以获取更多错误信息

