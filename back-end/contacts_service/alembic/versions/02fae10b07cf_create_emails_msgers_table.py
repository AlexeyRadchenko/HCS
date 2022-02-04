"""create emails_msgers table

Revision ID: 02fae10b07cf
Revises: efc78ecf9412
Create Date: 2022-02-04 12:39:35.571683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02fae10b07cf'
down_revision = 'efc78ecf9412'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'emails_msgers',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(50), nullable=True),
    )


def downgrade():
    op.drop_table('emails_msgers')
