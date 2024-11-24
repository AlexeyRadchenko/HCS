"""create table management_users_scopes

Revision ID: ad9b6e0537cd
Revises: 93a9e495f418
Create Date: 2022-01-17 15:35:26.304623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad9b6e0537cd'
down_revision = '93a9e495f418'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'management_users_scopes',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('management_users.id'), primary_key=True, nullable=False),
        sa.Column('scope_id', sa.Integer(), sa.ForeignKey('management_scopes.id'), primary_key=True, nullable=False),
        sa.Column('notes', sa.String, nullable=True)
    )



def downgrade():
    op.drop_table("management_users_scopes")
