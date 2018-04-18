"""Add users table

Revision ID: 1908608666b5
Revises:
Create Date: 2018-04-15 13:07:26.762294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1908608666b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('users')
