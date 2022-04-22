"""create account_scopes table

Revision ID: 8d826649522a
Revises: 676edd57bc42
Create Date: 2022-04-21 13:06:09.803233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d826649522a'
down_revision = '676edd57bc42'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "account_scopes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scope_name", sa.String(), nullable=True),
        sa.Column("active_scope", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table('account_scopes')
