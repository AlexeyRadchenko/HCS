"""create emails_msgers table

Revision ID: 365eb0a0d91a
Revises: e280519bcd33
Create Date: 2022-02-11 13:46:05.129001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '365eb0a0d91a'
down_revision = 'e280519bcd33'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'emails_msgers',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        #sa.Column('client_uuid', UUID(as_uuid=True), sa.ForeignKey('clients.uuid'), nullable=False), # use in postgress db
        sa.Column('client_uuid', sa.Text(length=36), sa.ForeignKey('clients.uuid'), nullable=False), # use for dev sqlite
        sa.Column('email', sa.String(50), nullable=True),
    )


def downgrade():
    op.drop_table('emails_msgers')
