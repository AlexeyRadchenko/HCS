"""create clients table

Revision ID: 194589433d66
Revises: 
Create Date: 2022-02-11 13:40:51.219236

"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = '194589433d66'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'clients',
        #sa.Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), # use in postgress db
        sa.Column('uuid', sa.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True), # use for dev sqlite
        sa.Column('name', sa.String(50), nullable=True),
        sa.Column('second_name', sa.String(50), nullable=True),
        sa.Column('surname', sa.String(50), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('client_del', sa.Boolean, default=False),
    )


def downgrade():
    op.drop_table('clients')
