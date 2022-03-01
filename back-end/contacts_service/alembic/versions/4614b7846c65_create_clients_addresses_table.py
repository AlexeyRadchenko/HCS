"""create clients_addresses table

Revision ID: 4614b7846c65
Revises: 1087208effd6
Create Date: 2022-02-11 13:52:22.001914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4614b7846c65'
down_revision = '1087208effd6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'clients_addresses',
        #sa.Column('client_uuid', UUID(as_uuid=True), sa.ForeignKey('clients.uuid'), primary_key=True, nullable=False), # use in postgress db
        sa.Column('client_uuid', sa.Text(length=36), sa.ForeignKey('clients.uuid'), primary_key=True, nullable=False), # use for dev sqlite
        sa.Column('address_id', sa.Integer(), sa.ForeignKey('addresses.id'), primary_key=True, nullable=False),
        sa.Column('full_owner', sa.Boolean, default=False),
        sa.Column('part_owner', sa.Boolean, default=False),
        sa.Column('part_size', sa.String, nullable=True),
    )


def downgrade():
    op.drop_table('clients_addresses')
