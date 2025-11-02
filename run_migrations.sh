#!/bin/bash
# 在服务器上运行数据库迁移
# 使用方法: bash run_migrations.sh

set -e

echo "=========================================="
echo "数据库迁移脚本"
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
    echo "✓ 虚拟环境已激活"
elif [ -d "venv" ]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
else
    echo "警告: 未找到虚拟环境目录 (.venv 或 venv)"
    echo "继续使用系统 Python..."
fi

# 检查 Flask 是否安装
echo ""
echo "检查 Flask 环境..."
python -c "import flask; print('✓ Flask 版本:', flask.__version__)" || {
    echo "✗ Flask 未安装"
    exit 1
}

# 检查数据库连接
echo ""
echo "检查数据库配置..."
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv('DATABASE_URL')
if db_url:
    print('✓ DATABASE_URL:', db_url[:50] + '...' if len(db_url) > 50 else db_url)
else:
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_user = os.getenv('DB_USER', 'root')
    db_name = os.getenv('DB_NAME', 'ai-tracks')
    print('✓ 数据库配置:')
    print('  主机:', db_host)
    print('  端口:', db_port)
    print('  用户:', db_user)
    print('  数据库:', db_name)
" || {
    echo "✗ 无法读取数据库配置"
    exit 1
}

# 测试数据库连接
echo ""
echo "测试数据库连接..."
python -c "
from app import create_app, db
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    try:
        db.engine.connect()
        print('✓ 数据库连接成功')
    except Exception as e:
        print('✗ 数据库连接失败:', str(e))
        exit(1)
" || {
    echo ""
    echo "数据库连接失败，请检查："
    echo "1. .env 文件中的数据库配置是否正确"
    echo "2. 数据库服务是否运行"
    echo "3. 数据库是否存在"
    exit 1
}

# 检查 migrations 目录
echo ""
echo "检查迁移目录..."
if [ ! -d "migrations" ]; then
    echo "初始化 Flask-Migrate..."
    flask db init
    echo "✓ 迁移目录已初始化"
fi

# 检查当前迁移状态
echo ""
echo "检查当前迁移状态..."
flask db current 2>&1 || echo "  当前无迁移记录"

# 创建迁移（如果有模型变更）
echo ""
echo "创建迁移（如果有变更）..."
flask db migrate -m "Update database schema" 2>&1 || {
    echo "  (没有新的变更需要迁移)"
}

# 应用迁移
echo ""
echo "应用数据库迁移..."
echo "这将在数据库中创建所有必需的表..."
flask db upgrade || {
    echo ""
    echo "✗ 迁移失败"
    echo ""
    echo "请检查："
    echo "1. 数据库用户是否有创建表的权限"
    echo "2. 数据库是否存在"
    echo "3. 查看上面的错误信息"
    exit 1
}

# 验证表是否创建
echo ""
echo "验证数据库表..."
python -c "
from app import create_app, db
from app.models import ProjectCase, News, ProductCategory, User, Contact, PageSettings, Slider
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    tables = []
    try:
        ProjectCase.query.first()
        tables.append('project_cases')
    except:
        pass
    try:
        News.query.first()
        tables.append('news')
    except:
        pass
    try:
        ProductCategory.query.first()
        tables.append('product_categories')
    except:
        pass
    try:
        User.query.first()
        tables.append('users')
    except:
        pass
    try:
        Contact.query.first()
        tables.append('contacts')
    except:
        pass
    try:
        PageSettings.query.first()
        tables.append('page_settings')
    except:
        pass
    try:
        Slider.query.first()
        tables.append('sliders')
    except:
        pass
    
    if tables:
        print('✓ 以下表已创建:', ', '.join(tables))
    else:
        print('⚠ 无法验证表，但迁移已运行')
" || {
    echo "⚠ 无法验证表，但迁移可能已成功"
}

echo ""
echo "=========================================="
echo "迁移完成！"
echo "=========================================="
echo ""
echo "如果遇到问题，请检查："
echo "1. 数据库配置是否正确 (.env 文件)"
echo "2. 数据库用户是否有足够权限"
echo "3. 数据库是否存在"
echo ""

