"""create client table

Revision ID: 5f234dfdbf28
Revises: 
Create Date: 2022-02-04 12:05:13.484817

"""
from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '5f234dfdbf28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key=True),
        #sa.Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), # use in postgress db
        sa.Column('uuid', sa.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True), # use for dev sqlite
        sa.Column('name', sa.String(50), nullable=True),
        sa.Column('second_name', sa.String(50), nullable=True),
        sa.Column('surname', sa.String(50), nullable=True),
        sa.Column('address', sa.Integer(), sa.ForeignKey('address.id'), nullable=True),
        sa.Column('phones', sa.Integer(), sa.ForeignKey('phones.id'), nullable=True),
        sa.Column('emails', sa.Integer(), sa.ForeignKey('emails_msgers.id'), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
    )


def downgrade():
    op.drop_table('clients')
