"""create client_organisation table

Revision ID: 025055e17255
Revises: d42620d81745
Create Date: 2022-02-08 12:36:44.301561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '025055e17255'
down_revision = 'd42620d81745'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'client_organisations',
        #sa.Column('client_uuid', UUID(as_uuid=True), sa.ForeignKey('clients.uuid'), primary_key=True, nullable=False), # use in postgress db
        sa.Column('client_uuid', sa.Text(length=36), sa.ForeignKey('clients.uuid'), primary_key=True, nullable=False), # use for dev sqlite
        sa.Column('org_id', sa.Integer(), sa.ForeignKey('organisations.id'), primary_key=True, nullable=False),
    )


def downgrade():
    op.drop_table('client_organisations')
