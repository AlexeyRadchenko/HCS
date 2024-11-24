"""edit actfiles and smetafiles table

Revision ID: 99be9396d53e
Revises: 63a8e9ae4fab
Create Date: 2024-10-30 16:05:00.175115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99be9396d53e'
down_revision: Union[str, None] = '63a8e9ae4fab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('actfiles', sa.Column('date_upload', sa.DateTime, server_default=sa.func.current_timestamp()))
    op.add_column('smetafiles', sa.Column('date_upload', sa.DateTime, server_default=sa.func.current_timestamp()))


def downgrade() -> None:
    op.drop_column('actfiles', 'date_upload')
    op.drop_column('smetafiles', 'date_upload')
