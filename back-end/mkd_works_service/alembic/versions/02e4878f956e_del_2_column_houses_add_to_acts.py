"""del 2 column houses, add to acts

Revision ID: 02e4878f956e
Revises: 99be9396d53e
Create Date: 2024-11-07 14:06:17.807863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02e4878f956e'
down_revision: Union[str, None] = '99be9396d53e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('houses', 'director')
    op.drop_column('houses', 'director_appartment')
    op.add_column('acts', sa.Column('director', sa.String))
    op.add_column('acts', sa.Column('director_appartment', sa.String))


def downgrade() -> None:
    op.drop_column('acts', 'director')
    op.drop_column('acts', 'director_appartment')
    op.add_column('houses', sa.Column('director', sa.String))
    op.add_column('houses', sa.Column('director_appartment', sa.String))
