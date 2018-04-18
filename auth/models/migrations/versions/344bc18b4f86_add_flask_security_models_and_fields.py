"""Add Flask Security Models and fields

Revision ID: 344bc18b4f86
Revises: 1908608666b5
Create Date: 2018-04-18 12:45:30.211169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '344bc18b4f86'
down_revision = '1908608666b5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'roles_users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column(
        'users',
        sa.Column('active', sa.Boolean(), nullable=True))
    op.add_column(
        'users',
        sa.Column('confirmed_at', sa.DateTime(), nullable=True))
    op.add_column(
        'users',
        sa.Column('current_login_at', sa.DateTime(), nullable=True))
    op.add_column(
        'users',
        sa.Column('current_login_ip', sa.String(length=100), nullable=True))
    op.add_column(
        'users',
        sa.Column('last_login_at', sa.DateTime(), nullable=True))
    op.add_column(
        'users',
        sa.Column('last_login_ip', sa.String(length=100), nullable=True))
    op.add_column(
        'users',
        sa.Column('login_count', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('users', 'login_count')
    op.drop_column('users', 'last_login_ip')
    op.drop_column('users', 'last_login_at')
    op.drop_column('users', 'current_login_ip')
    op.drop_column('users', 'current_login_at')
    op.drop_column('users', 'confirmed_at')
    op.drop_column('users', 'active')
    op.drop_table('roles_users')
    op.drop_table('roles')
