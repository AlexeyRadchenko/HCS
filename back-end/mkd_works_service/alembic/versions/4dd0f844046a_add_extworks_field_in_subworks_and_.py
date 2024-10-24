"""add extworks field in subworks and fixworks table

Revision ID: 4dd0f844046a
Revises: 132556611850
Create Date: 2024-10-24 15:08:09.279330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dd0f844046a'
down_revision: Union[str, None] = '132556611850'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('subworks', sa.Column('ext_works', sa.String))
    op.add_column('fixworks', sa.Column('ext_works', sa.String))


def downgrade() -> None:
    op.drop_column('subworks', 'ext_works')
    op.drop_column('fixworks', 'ext_works')
