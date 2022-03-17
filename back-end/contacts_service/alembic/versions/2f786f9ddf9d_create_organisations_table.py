"""create organisations table

Revision ID: 2f786f9ddf9d
Revises: 4614b7846c65
Create Date: 2022-02-11 13:53:38.485910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f786f9ddf9d'
down_revision = '4614b7846c65'
branch_labels = None
depends_on = None

from sqlalchemy.dialects.postgresql import UUID

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
"""
def upgrade():
    op.create_table(
        'organisations',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('full_name', sa.String(300), nullable=True),
        sa.Column('short_name', sa.String(150), nullable=True)
    )


def downgrade():
    op.drop_table('organisations')"""
