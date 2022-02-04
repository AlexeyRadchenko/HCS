"""create address table

Revision ID: a120fda9848c
Revises: 5f234dfdbf28
Create Date: 2022-02-04 12:30:55.576857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a120fda9848c'
down_revision = '5f234dfdbf28'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'address',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('street', sa.String(50), nullable=True),
        sa.Column('house_number', sa.String(50), nullable=True),
        sa.Column('entrance', sa.String(50), nullable=True),
        sa.Column('appartment', sa.String(50), nullable=True),
    )


def downgrade():
    op.drop_table('address')
