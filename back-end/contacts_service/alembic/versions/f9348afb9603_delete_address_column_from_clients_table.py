"""delete address column from clients table

Revision ID: f9348afb9603
Revises: 02fae10b07cf
Create Date: 2022-02-04 13:37:44.375885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9348afb9603'
down_revision = '02fae10b07cf'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.drop_column('address')


def downgrade():
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.Integer(), sa.ForeignKey('address.id'), nullable=True))
