"""Add UUID to user

Revision ID: 99f9d0ecec10
Revises: 344bc18b4f86
Create Date: 2018-04-23 08:35:06.401614

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy import select

# revision identifiers, used by Alembic.
revision = '99f9d0ecec10'
down_revision = '344bc18b4f86'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('uuid', sa.String(), nullable=True))

    user_table = sa.Table(
        'users',
        sa.MetaData(bind=op.get_bind()), autoload=True)

    # Add uuids to existing users
    ids = op.get_bind().execute(select([user_table.c.id]))
    for id_tuple in ids:
        id = id_tuple[0]
        op.get_bind().execute(
            user_table.update()
            .values(uuid=uuid.uuid4())
            .where(user_table.c.id == id)
        )

    op.alter_column('users', 'uuid', nullable=False)
    op.create_unique_constraint(None, 'users', ['uuid'])


def downgrade():
    op.drop_column('users', 'uuid')
