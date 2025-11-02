"""Create initial tables for project_cases, contacts, news, case_photos, sliders

Revision ID: 000000000001
Revises: a34c0bbd7656
Create Date: 2025-11-02 08:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '000000000001'
down_revision = 'a34c0bbd7656'
branch_labels = None
depends_on = None


def table_exists(table_name):
    """Check if a table exists in the database."""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def upgrade():
    # Create project_cases table
    if not table_exists('project_cases'):
        op.create_table('project_cases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False, comment='名稱'),
        sa.Column('sub_name', sa.String(length=255), nullable=True, comment='副標題'),
        sa.Column('url', sa.String(length=255), nullable=True, comment='網址'),
        sa.Column('content', sa.Text(), nullable=False, comment='內容'),
        sa.Column('status', sa.Boolean(), nullable=False, comment='狀態'),
        sa.Column('views', sa.Integer(), nullable=False, server_default='0', comment='閱讀次數'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
        )
        print("Created table 'project_cases'")
    else:
        print("Table 'project_cases' already exists, skipping")
    
    # Create case_photos table
    if not table_exists('case_photos'):
        op.create_table('case_photos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_case_id', sa.Integer(), nullable=False),
        sa.Column('image', sa.String(length=255), nullable=False, comment='案例照片'),
        sa.Column('sort_order', sa.Integer(), nullable=False, comment='排序'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_case_id'], ['project_cases.id'], ondelete='CASCADE')
        )
        print("Created table 'case_photos'")
    else:
        print("Table 'case_photos' already exists, skipping")
    
    # Create contacts table
    if not table_exists('contacts'):
        op.create_table('contacts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False, comment='姓名'),
        sa.Column('email', sa.String(length=255), nullable=False, comment='信箱'),
        sa.Column('phone', sa.String(length=20), nullable=True, comment='電話'),
        sa.Column('subject', sa.String(length=255), nullable=False, comment='主旨'),
        sa.Column('message', sa.Text(), nullable=False, comment='訊息'),
        sa.Column('status', sa.Enum('pending', 'processing', 'completed', name='contact_status'), 
                  nullable=False, comment='處理狀態'),
        sa.Column('reply', sa.Text(), nullable=True, comment='回覆內容'),
        sa.Column('replied_at', sa.DateTime(), nullable=True, comment='回覆時間'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
        )
        print("Created table 'contacts'")
    else:
        print("Table 'contacts' already exists, skipping")
    
    # Create news table
    if not table_exists('news'):
        op.create_table('news',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False, comment='標題'),
        sa.Column('content', sa.Text(), nullable=False, comment='內容'),
        sa.Column('published_at', sa.Date(), nullable=False, comment='發布日期'),
        sa.Column('is_active', sa.Boolean(), nullable=False, comment='是否啟用'),
        sa.Column('views', sa.Integer(), nullable=False, server_default='0', comment='閱讀次數'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
        )
        print("Created table 'news'")
    else:
        print("Table 'news' already exists, skipping")
    
    # Create sliders table
    if not table_exists('sliders'):
        op.create_table('sliders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False, comment='標題'),
        sa.Column('description', sa.Text(), nullable=True, comment='描述'),
        sa.Column('image', sa.String(length=255), nullable=False, comment='圖片'),
        sa.Column('link', sa.String(length=255), nullable=True, comment='連結'),
        sa.Column('sort', sa.Integer(), nullable=False, comment='排序'),
        sa.Column('is_active', sa.Boolean(), nullable=False, comment='是否啟用'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
        )
        print("Created table 'sliders'")
    else:
        print("Table 'sliders' already exists, skipping")


def downgrade():
    # Drop tables in reverse order
    if table_exists('sliders'):
        op.drop_table('sliders')
    if table_exists('news'):
        op.drop_table('news')
    if table_exists('contacts'):
        op.drop_table('contacts')
    if table_exists('case_photos'):
        op.drop_table('case_photos')
    if table_exists('project_cases'):
        op.drop_table('project_cases')

