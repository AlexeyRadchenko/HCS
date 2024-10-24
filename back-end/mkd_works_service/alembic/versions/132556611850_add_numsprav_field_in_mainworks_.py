"""add numSprav field in mainworks, subworks and fixworks table

Revision ID: 132556611850
Revises: 6eda9fec2694
Create Date: 2024-10-24 09:04:05.097668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '132556611850'
down_revision: Union[str, None] = '6eda9fec2694'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('mainworks', sa.Column('numsprav', sa.String))
    op.add_column('subworks', sa.Column('numsprav', sa.String))
    op.add_column('fixworks', sa.Column('numsprav', sa.String))


def downgrade() -> None:
    op.drop_column('mainworks', 'numsprav')
    op.drop_column('subworks', 'numsprav')
    op.drop_column('fixworks', 'numsprav')
