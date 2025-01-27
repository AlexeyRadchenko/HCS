"""add director and dir appartment field to houses table

Revision ID: 2d4dd486e643
Revises: 98bdd7973834
Create Date: 2025-01-27 08:55:26.862231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d4dd486e643'
down_revision: Union[str, None] = '98bdd7973834'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('houses', sa.Column('director_fio', sa.String))
    op.add_column('houses', sa.Column('director_appartment', sa.String))


def downgrade() -> None:
    op.drop_column('houses', 'director_fio')
    op.drop_column('houses', 'director_appartment')
