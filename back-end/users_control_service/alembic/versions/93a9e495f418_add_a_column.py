"""Add a column

Revision ID: 93a9e495f418
Revises: 77d1d084967c
Create Date: 2022-01-17 15:05:47.206880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93a9e495f418'
down_revision = '77d1d084967c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "management_scopes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scope_name", sa.String(), nullable=True),
        sa.Column("active_scope", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table('scopes')
