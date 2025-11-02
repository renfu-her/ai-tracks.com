#!/bin/bash
# 强制运行数据库迁移 - 创建所有缺失的表
# 使用方法: bash force_migrate.sh

set -e

echo "=========================================="
echo "强制运行数据库迁移"
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
else
    echo "警告: 未找到虚拟环境"
    exit 1
fi

# 设置环境变量
export FLASK_ENV=production

echo ""
echo "检查当前迁移状态..."
flask db current 2>&1 || echo "  无迁移记录"

echo ""
echo "查看迁移历史..."
flask db history | head -20

echo ""
echo "检查数据库中的表..."
python -c "
from app import create_app, db
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print('已存在的表:', ', '.join(sorted(tables)) if tables else '无')
    
    required_tables = ['project_cases', 'contacts', 'news', 'case_photos', 'sliders', 'users', 'product_categories', 'page_settings']
    missing = [t for t in required_tables if t not in tables]
    if missing:
        print('缺失的表:', ', '.join(missing))
    else:
        print('✓ 所有必需的表都存在')
" || {
    echo "无法连接到数据库"
    exit 1
}

echo ""
echo "=========================================="
echo "开始运行迁移..."
echo "=========================================="

# 尝试运行迁移
echo ""
echo "运行 flask db upgrade..."
flask db upgrade || {
    echo ""
    echo "迁移失败，尝试修复..."
    
    # 检查 alembic_version 表
    echo ""
    echo "检查迁移版本表..."
    python -c "
from app import create_app, db
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    inspector = db.inspect(db.engine)
    if 'alembic_version' in inspector.get_table_names():
        result = db.session.execute(db.text('SELECT version_num FROM alembic_version'))
        version = result.scalar()
        print('当前迁移版本:', version if version else '无')
    else:
        print('alembic_version 表不存在')
    "
    
    echo ""
    echo "如果迁移失败，可能需要手动标记迁移版本。"
    echo "请运行以下 SQL 命令（如果表已存在）："
    echo ""
    echo "USE blog;"
    echo "INSERT INTO alembic_version (version_num) VALUES ('000000000001')"
    echo "ON DUPLICATE KEY UPDATE version_num = '000000000001';"
    echo ""
    echo "然后再次运行: flask db upgrade"
    exit 1
}

echo ""
echo "=========================================="
echo "验证迁移结果"
echo "=========================================="

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
    
    # 检查 project_cases 表结构
    if 'project_cases' in tables:
        columns = [col['name'] for col in inspector.get_columns('project_cases')]
        print('')
        print('project_cases 表的列:', ', '.join(columns))
"

echo ""
echo "=========================================="
echo "迁移完成！"
echo "=========================================="
echo ""
echo "如果表仍然缺失，请："
echo "1. 检查迁移日志中的错误信息"
echo "2. 确认数据库用户有创建表的权限"
echo "3. 手动运行 SQL 创建表（参考模型定义）"
echo ""

