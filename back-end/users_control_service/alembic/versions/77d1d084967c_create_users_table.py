"""create users table

Revision ID: 77d1d084967c
Revises: 
Create Date: 2022-01-12 11:39:42.199660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77d1d084967c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "management_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("login", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("second_name", sa.String(), nullable=True),
        sa.Column("surname", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_management_users_email"), "management_users", ["email"], unique=True)
    op.create_index(op.f("ix_management_users_login"), "management_users", ["login"], unique=True)
    op.create_index(op.f("ix_management_users_id"), "management_users", ["id"], unique=False)
    

def downgrade():
    op.drop_index(op.f("ix_management_users_id"), table_name="management_users")
    op.drop_index(op.f("ix_management_users_login"), table_name="management_users")
    op.drop_index(op.f("ix_management_users_email"), table_name="management_users")
    op.drop_table("management_users")
