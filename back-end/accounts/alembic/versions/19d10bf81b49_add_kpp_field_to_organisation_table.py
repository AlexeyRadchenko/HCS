"""add kpp field to organisation table

Revision ID: 19d10bf81b49
Revises: c2e9b98a73eb
Create Date: 2022-05-25 11:53:48.234805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19d10bf81b49'
down_revision = 'c2e9b98a73eb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "organisation",
        sa.Column("inn", sa.String(), nullable=True),
    )


def downgrade():
    op.drop_column('organisation', 'inn')
