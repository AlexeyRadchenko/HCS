"""create middle table accounts_electric_counters table

Revision ID: 6da99ab6aa17
Revises: c389864400f2
Create Date: 2022-05-20 12:30:22.275398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6da99ab6aa17'
down_revision = 'c389864400f2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'accounts_electric_counters',
        sa.Column('account_id', sa.BigInteger(), sa.ForeignKey('account.id'), primary_key=True),
        sa.Column('counter_id', sa.BigInteger(), sa.ForeignKey('electric_counter.id'), primary_key=True),
    )



def downgrade():
    op.drop_table("accounts_electric_counters")
