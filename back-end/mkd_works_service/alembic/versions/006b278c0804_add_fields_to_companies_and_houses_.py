"""add fields to companies and houses tables

Revision ID: 006b278c0804
Revises: 03c93464a0dc
Create Date: 2024-11-13 11:39:39.264488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '006b278c0804'
down_revision: Union[str, None] = '03c93464a0dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('companies', sa.Column('dirname_who_what', sa.String(500)))
    op.add_column('companies', sa.Column('dirsurname_who_what', sa.String(500)))
    op.add_column('companies', sa.Column('dirsecondname_who_what', sa.String(500)))
    op.add_column('houses', sa.Column('house_square', sa.Numeric, nullable=True))


def downgrade() -> None:
    op.drop_column('companies', 'dirname_who_what')
    op.drop_column('companies', 'dirsurname_who_what')
    op.drop_column('companies', 'dirsecondname_who_what')
    op.drop_column('companies', 'house_square')
 
