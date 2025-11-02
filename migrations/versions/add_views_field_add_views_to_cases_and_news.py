"""Add views field to project_cases and news tables

Revision ID: add_views_field
Revises: ed9a3a646336
Create Date: 2025-11-02 08:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = 'add_views_field'
down_revision = 'ed9a3a646336'
branch_labels = None
depends_on = None


def table_exists(table_name):
    """Check if a table exists in the database."""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def column_exists(table_name, column_name):
    """Check if a column exists in a table."""
    bind = op.get_bind()
    inspector = inspect(bind)
    if table_name not in inspector.get_table_names():
        return False
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade():
    # Add views column to project_cases table
    if table_exists('project_cases'):
        if not column_exists('project_cases', 'views'):
            with op.batch_alter_table('project_cases', schema=None) as batch_op:
                batch_op.add_column(sa.Column('views', sa.Integer(), nullable=False, server_default='0', comment='閱讀次數'))
            print("Added 'views' column to 'project_cases' table")
        else:
            print("Column 'views' already exists in 'project_cases', skipping")
    
    # Add views column to news table
    if table_exists('news'):
        if not column_exists('news', 'views'):
            with op.batch_alter_table('news', schema=None) as batch_op:
                batch_op.add_column(sa.Column('views', sa.Integer(), nullable=False, server_default='0', comment='閱讀次數'))
            print("Added 'views' column to 'news' table")
        else:
            print("Column 'views' already exists in 'news', skipping")


def downgrade():
    # Remove views column from news table
    if table_exists('news'):
        if column_exists('news', 'views'):
            with op.batch_alter_table('news', schema=None) as batch_op:
                batch_op.drop_column('views')
    
    # Remove views column from project_cases table
    if table_exists('project_cases'):
        if column_exists('project_cases', 'views'):
            with op.batch_alter_table('project_cases', schema=None) as batch_op:
                batch_op.drop_column('views')

