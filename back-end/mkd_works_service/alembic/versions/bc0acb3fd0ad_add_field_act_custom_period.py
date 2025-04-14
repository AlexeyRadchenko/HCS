"""add field act_custom_period

Revision ID: bc0acb3fd0ad
Revises: 2d4dd486e643
Create Date: 2025-02-19 09:42:45.219504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc0acb3fd0ad'
down_revision: Union[str, None] = '2d4dd486e643'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('acthasmainworks', sa.Column('act_custom_period', sa.String))
    op.add_column('acthassubworks', sa.Column('act_custom_period', sa.String))
    op.add_column('acthasfixworks', sa.Column('act_custom_period', sa.String))


def downgrade() -> None:
    op.drop_column('acthasmainworks', 'act_custom_period')
    op.drop_column('acthassubworks', 'act_custom_period')
    op.drop_column('acthasfixworks', 'act_custom_period')
