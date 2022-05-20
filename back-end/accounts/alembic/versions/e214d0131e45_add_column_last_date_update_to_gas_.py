"""add column last_date_update to gas_counter table

Revision ID: e214d0131e45
Revises: fb2488c7ab06
Create Date: 2022-05-20 11:29:00.019748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e214d0131e45'
down_revision = 'fb2488c7ab06'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "gas_counter",
        sa.Column("last_date_update", sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_column('gas_counter', 'last_date_update')
