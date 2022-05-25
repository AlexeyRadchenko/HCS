"""add kpp field to organisation table

Revision ID: c2e9b98a73eb
Revises: 6da99ab6aa17
Create Date: 2022-05-25 11:48:34.999932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2e9b98a73eb'
down_revision = '6da99ab6aa17'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "organisation",
        sa.Column("kpp", sa.String(), nullable=True),
    )


def downgrade():
    op.drop_column('organisation', 'kpp')
