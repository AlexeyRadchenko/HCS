"""add columns to account_users table

Revision ID: 7c4c92dc6df9
Revises: 8b00bce0f55f
Create Date: 2022-04-21 13:43:28.130771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c4c92dc6df9'
down_revision = '8b00bce0f55f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('account_users', sa.Column('street', sa.String, nullable=True))
    op.add_column('account_users', sa.Column('house', sa.String, nullable=True))
    op.add_column('account_users', sa.Column('appartment', sa.String, nullable=True))

def downgrade():
    op.drop_column('account_users', 'street')
    op.drop_column('account_users', 'house')
    op.drop_column('account_users', 'appartment')
