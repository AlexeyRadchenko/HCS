"""add notes field to acthas... tables

Revision ID: 98bdd7973834
Revises: 117e6051e947
Create Date: 2025-01-27 08:04:41.932991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98bdd7973834'
down_revision: Union[str, None] = '117e6051e947'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('acthasmainworks', sa.Column('notes', sa.String))
    op.add_column('acthassubworks', sa.Column('notes', sa.String))
    op.add_column('acthasfixworks', sa.Column('notes', sa.String))


def downgrade() -> None:
    op.drop_column('acthasmainworks', 'notes')
    op.drop_column('acthassubworks', 'notes')
    op.drop_column('acthasfixworks', 'notes')
