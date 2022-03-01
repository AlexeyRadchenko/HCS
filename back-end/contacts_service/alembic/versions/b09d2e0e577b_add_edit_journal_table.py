"""add edit_journal table

Revision ID: b09d2e0e577b
Revises: ae45f1875cde
Create Date: 2022-02-22 11:12:39.695086

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'b09d2e0e577b'
down_revision = 'ae45f1875cde'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'edit_journal',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        #sa.Column('client_uuid', UUID(as_uuid=True), sa.ForeignKey('clients.uuid'), nullable=False), # use in postgress db
        sa.Column('client_uuid', sa.Text(length=36), sa.ForeignKey('clients.uuid'), nullable=False), # use for dev sqlite
        sa.Column('date_create', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('date_update', sa.DateTime(), nullable=True),
        sa.Column('date_delete', sa.DateTime(), nullable=True),
        sa.Column('who_make', sa.String(100), nullable=False),
        sa.Column('who_update', sa.String(100), nullable=True),
        sa.Column('who_delete', sa.String(100), nullable=True),
    )


def downgrade():
    op.drop_table('edit_journal')
