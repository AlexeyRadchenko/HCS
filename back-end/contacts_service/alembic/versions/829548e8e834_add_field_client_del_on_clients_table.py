"""add field client_del on clients table

Revision ID: 829548e8e834
Revises: 025055e17255
Create Date: 2022-02-09 12:19:30.681918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '829548e8e834'
down_revision = '025055e17255'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('clients', sa.Column('client_del', sa.Boolean(), default=False))


def downgrade():
    op.drop_column('clients', 'client_del')
