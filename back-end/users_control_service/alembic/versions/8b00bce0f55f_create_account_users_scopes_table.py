"""create account_users_scopes table

Revision ID: 8b00bce0f55f
Revises: 8d826649522a
Create Date: 2022-04-21 13:10:43.404296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b00bce0f55f'
down_revision = '8d826649522a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'account_users_scopes',
        sa.Column('account_id', sa.Integer(), sa.ForeignKey('account_users.id'), primary_key=True, nullable=False),
        sa.Column('scope_id', sa.Integer(), sa.ForeignKey('account_scopes.id'), primary_key=True, nullable=False),
        sa.Column('notes', sa.String, nullable=True)
    )



def downgrade():
    op.drop_table("account_users_scopes")
