"""add column type to water_counter table

Revision ID: f30895a3deb0
Revises: 7b73316efabc
Create Date: 2022-05-16 12:07:13.451204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f30895a3deb0'
down_revision = '7b73316efabc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "water_counter",
        sa.Column("type", sa.String(), nullable=True),
    )


def downgrade():
    op.drop_column('water_counter', 'type')

