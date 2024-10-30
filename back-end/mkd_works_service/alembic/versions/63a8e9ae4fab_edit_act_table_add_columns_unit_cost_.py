"""edit act table add columns unit_cost andwork_square

Revision ID: 63a8e9ae4fab
Revises: 4dd0f844046a
Create Date: 2024-10-30 11:52:04.407553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63a8e9ae4fab'
down_revision: Union[str, None] = '4dd0f844046a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('acts', sa.Column('unit_cost', sa.String))
    op.add_column('acts', sa.Column('work_square', sa.String))

def downgrade() -> None:
    op.drop_column('acts', 'unit_cost')
    op.drop_column('acts', 'work_square')
