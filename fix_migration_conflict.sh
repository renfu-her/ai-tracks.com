#!/bin/bash
# 修复迁移冲突脚本
# 当表已存在但迁移记录显示未创建时使用

set -e

echo "=========================================="
echo "修复迁移冲突"
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
echo "检查数据库中的表..."
python -c "
from app import create_app, db
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print('已存在的表:')
    for table in sorted(tables):
        print('  -', table)
    
    # 检查关键表
    key_tables = ['product_categories', 'project_cases', 'users', 'news', 'contacts', 'page_settings']
    missing_tables = [t for t in key_tables if t not in tables]
    if missing_tables:
        print('\n缺失的表:', ', '.join(missing_tables))
    else:
        print('\n所有关键表都存在')
" || {
    echo "无法连接到数据库"
    exit 1
}

echo ""
echo "检查迁移版本..."
flask db current 2>&1 || echo "  当前无迁移记录"

echo ""
echo "检查迁移历史..."
flask db history | head -10

echo ""
echo "=========================================="
echo "选择修复方法:"
echo "=========================================="
echo "1. 运行修复后的迁移（推荐）- 已修改迁移文件以检查表是否存在"
echo "2. 手动标记迁移为已完成"
echo "3. 查看详细错误信息"
echo ""
read -p "请选择 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "运行修复后的迁移..."
        flask db upgrade || {
            echo ""
            echo "如果仍然失败，请尝试方法 2"
        }
        ;;
    2)
        echo ""
        echo "手动标记迁移为已完成..."
        echo ""
        echo "请在 MySQL 中执行以下 SQL 命令:"
        echo ""
        echo "USE blog;"
        echo "INSERT INTO alembic_version (version_num) VALUES ('32914cc96883')"
        echo "ON DUPLICATE KEY UPDATE version_num = '32914cc96883';"
        echo ""
        echo "然后运行: flask db upgrade"
        ;;
    3)
        echo ""
        echo "运行迁移以查看详细错误..."
        flask db upgrade
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "验证修复结果"
echo "=========================================="

python -c "
from app import create_app, db
import os
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    
    # 检查关键表
    key_tables = ['product_categories', 'project_cases', 'users', 'news', 'contacts', 'page_settings']
    existing = [t for t in key_tables if t in tables]
    missing = [t for t in key_tables if t not in tables]
    
    print('已存在的关键表:', len(existing), '/', len(key_tables))
    if missing:
        print('缺失的表:', ', '.join(missing))
    else:
        print('✓ 所有关键表都存在')
    
    # 检查 project_cases 表是否有 category_id 列
    if 'project_cases' in tables:
        columns = [col['name'] for col in inspector.get_columns('project_cases')]
        if 'category_id' in columns:
            print('✓ project_cases.category_id 列存在')
        else:
            print('✗ project_cases.category_id 列不存在')
"

echo ""
echo "修复完成！"

