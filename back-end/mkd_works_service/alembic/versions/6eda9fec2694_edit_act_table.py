"""edit act table

Revision ID: 6eda9fec2694
Revises: 9a1d8cacf8f4
Create Date: 2024-10-22 07:03:57.601042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6eda9fec2694'
down_revision: Union[str, None] = '9a1d8cacf8f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('acts', sa.Column('month_year_works', sa.Date))

def downgrade() -> None:
    op.drop_column('acts', 'month_year_works')
