"""create account table

Revision ID: 676edd57bc42
Revises: ad9b6e0537cd
Create Date: 2022-04-21 13:00:11.617595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '676edd57bc42'
down_revision = 'ad9b6e0537cd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "account_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("account", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("second_name", sa.String(), nullable=True),
        sa.Column("surname", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_account_users_email"), "account_users", ["email"], unique=True)
    op.create_index(op.f("ix_account_users_id"), "account_users", ["id"], unique=False)
    

def downgrade():
    op.drop_index(op.f("ix_account_users_id"), table_name="account_users")
    op.drop_index(op.f("ix_account_users_email"), table_name="account_users")
    op.drop_table("account_users")
