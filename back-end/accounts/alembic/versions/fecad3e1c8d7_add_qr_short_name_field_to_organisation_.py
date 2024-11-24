"""add qr_short_name field to organisation table

Revision ID: fecad3e1c8d7
Revises: 19d10bf81b49
Create Date: 2022-05-25 14:18:46.371168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fecad3e1c8d7'
down_revision = '19d10bf81b49'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "organisation",
        sa.Column("qr_short_name", sa.String(), nullable=True),
    )


def downgrade():
    op.drop_column('organisation', 'qr_short_name')
