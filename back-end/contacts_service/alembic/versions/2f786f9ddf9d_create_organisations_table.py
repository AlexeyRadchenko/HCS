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


def upgrade():
    op.create_table(
        'organisations',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('full_name', sa.String(300), nullable=True),
        sa.Column('short_name', sa.String(150), nullable=True)
    )


def downgrade():
    op.drop_table('organisations')
