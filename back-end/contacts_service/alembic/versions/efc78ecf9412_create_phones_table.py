"""create phones table

Revision ID: efc78ecf9412
Revises: a120fda9848c
Create Date: 2022-02-04 12:36:48.673456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efc78ecf9412'
down_revision = 'a120fda9848c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'phones',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('home_phone', sa.String(50), nullable=True),
        sa.Column('work_phone', sa.String(50), nullable=True),
        sa.Column('mobile_phone', sa.String(50), nullable=True),
    )


def downgrade():
    op.drop_table('phones')
