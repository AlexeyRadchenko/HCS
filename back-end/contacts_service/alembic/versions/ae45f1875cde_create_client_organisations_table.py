"""create client_organisations table

Revision ID: ae45f1875cde
Revises: 2f786f9ddf9d
Create Date: 2022-02-11 13:54:11.859274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae45f1875cde'
down_revision = '2f786f9ddf9d'
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
