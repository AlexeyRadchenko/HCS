"""create electric_counter table

Revision ID: c389864400f2
Revises: e214d0131e45
Create Date: 2022-05-20 12:13:06.886587

"""
from xmlrpc.client import Boolean, DateTime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c389864400f2'
down_revision = 'e214d0131e45'
branch_labels = None
depends_on = None

    
def upgrade():
    op.create_table(
        'electric_counter',
        sa.Column('id', sa.BigInteger(), primary_key=True, index=True, nullable=False, autoincrement=True),
        sa.Column('outer_base_id', sa.BigInteger(), nullable=True),
        sa.Column('setup_date', sa.DateTime(), nullable=True),
        sa.Column('in_work', sa.Boolean(), default=True),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('serial_number', sa.String(), nullable=True),
        sa.Column('simple_data', sa.Integer(), nullable=True),
        sa.Column('day_data', sa.Integer(), nullable=True),
        sa.Column('night_data', sa.Integer(), nullable=True),
        sa.Column('old_simple_data', sa.Integer(), nullable=True),
        sa.Column('old_day_data', sa.Integer(), nullable=True),
        sa.Column('old_night_data', sa.Integer(), nullable=True),
        sa.Column('simple_diff', sa.Integer(), nullable=True),
        sa.Column('day_diff', sa.Integer(), nullable=True),
        sa.Column('night_diff', sa.Integer(), nullable=True),
        sa.Column('date_update', sa.DateTime(), nullable=True),
        sa.Column('last_date_update', sa.DateTime(), nullable=True),
        sa.Column('who_last_modify', sa.String(), nullable=True),
    )



def downgrade():
    op.drop_table("electric_counter")
