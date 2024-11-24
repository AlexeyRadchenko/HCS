"""add column last_date_update to water_counter table

Revision ID: fb2488c7ab06
Revises: f30895a3deb0
Create Date: 2022-05-16 15:39:24.515452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb2488c7ab06'
down_revision = 'f30895a3deb0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "water_counter",
        sa.Column("last_date_update", sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_column('water_counter', 'last_date_update')
