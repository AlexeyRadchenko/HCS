"""create phones table

Revision ID: e280519bcd33
Revises: 194589433d66
Create Date: 2022-02-11 13:44:41.834772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e280519bcd33'
down_revision = '194589433d66'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'phones',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        #sa.Column('client_uuid', UUID(as_uuid=True), sa.ForeignKey('clients.uuid'), nullable=False), # use in postgress db
        sa.Column('client_uuid', sa.Text(length=36), sa.ForeignKey('clients.uuid'), nullable=False), # use for dev sqlite
        sa.Column('home_phone', sa.String(50), nullable=True),
        sa.Column('work_phone', sa.String(50), nullable=True),
        sa.Column('mobile_phone', sa.String(50), nullable=True),
    )


def downgrade():
    op.drop_table('phones')
