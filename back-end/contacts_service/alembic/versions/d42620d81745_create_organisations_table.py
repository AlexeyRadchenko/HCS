"""create organisations table

Revision ID: d42620d81745
Revises: ae6bc5f93ff8
Create Date: 2022-02-08 12:33:19.269937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd42620d81745'
down_revision = 'ae6bc5f93ff8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'organisations',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('full_name', sa.String(300), nullable=True),
        sa.Column('short_name', sa.String(150), nullable=True)
    )


def downgrade():
    op.drop_table('organisations')
