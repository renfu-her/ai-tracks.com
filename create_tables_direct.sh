#!/bin/bash
# 使用 SQL 直接创建表（迁移失败时的备选方案）
# 使用方法: bash create_tables_direct.sh

set -e

echo "=========================================="
echo "直接创建数据库表"
echo "=========================================="

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "当前目录: $SCRIPT_DIR"
echo ""

# 激活虚拟环境
if [ -d ".venv" ]; then
    echo "激活虚拟环境..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
fi

# 设置环境变量
export FLASK_ENV=production

echo ""
echo "读取数据库配置..."
DB_CONFIG=$(python -c "
import os
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv('DATABASE_URL')
if db_url:
    print(db_url)
else:
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'ai-tracks')
    
    if db_password:
        print(f'{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    else:
        print(f'{db_user}@{db_host}:{db_port}/{db_name}')
")

echo "数据库配置: $DB_CONFIG"
echo ""

# 检查 SQL 文件是否存在
SQL_FILE="$SCRIPT_DIR/create_tables.sql"
if [ ! -f "$SQL_FILE" ]; then
    echo "错误: create_tables.sql 文件不存在"
    exit 1
fi

echo "使用 SQL 文件创建表: $SQL_FILE"
echo ""
echo "请手动执行以下命令:"
echo ""
echo "mysql -u root -p blog < create_tables.sql"
echo ""
echo "或者："
echo ""
echo "mysql -u root -p"
echo "USE blog;"
echo "SOURCE create_tables.sql;"
echo ""

read -p "是否已创建表？(y/n): " response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    echo "验证表是否创建..."
    python -c "
from app import create_app, db
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    
    required_tables = ['project_cases', 'contacts', 'news', 'case_photos', 'sliders', 'users', 'product_categories', 'page_settings']
    existing = [t for t in required_tables if t in tables]
    missing = [t for t in required_tables if t not in tables]
    
    print('已存在的表:', len(existing), '/', len(required_tables))
    for table in existing:
        print('  ✓', table)
    
    if missing:
        print('缺失的表:', ', '.join(missing))
    else:
        print('')
        print('✓ 所有必需的表都已创建！')
    "
else
    echo "请先创建表，然后重新运行此脚本"
fi

echo ""
echo "完成！"

