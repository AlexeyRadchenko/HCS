"""create clients_address table

Revision ID: ae6bc5f93ff8
Revises: f9348afb9603
Create Date: 2022-02-04 13:50:37.594443

"""
from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'ae6bc5f93ff8'
down_revision = 'f9348afb9603'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'clients_address',
        #sa.Column('client_uuid', UUID(as_uuid=True), sa.ForeignKey('clients.uuid'), primary_key=True, nullable=False), # use in postgress db
        sa.Column('client_uuid', sa.Text(length=36), sa.ForeignKey('clients.uuid'), primary_key=True, nullable=False), # use for dev sqlite
        sa.Column('address_id', sa.Integer(), sa.ForeignKey('address.id'), primary_key=True, nullable=False),
        sa.Column('full_owner', sa.Boolean, default=False),
        sa.Column('part_owner', sa.Boolean, default=False),
        sa.Column('part_size', sa.String, nullable=True),
    )


def downgrade():
    op.drop_table('clients_address')
