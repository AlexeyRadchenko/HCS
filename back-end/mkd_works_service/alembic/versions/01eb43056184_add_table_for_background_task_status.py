"""add table for background task status

Revision ID: 01eb43056184
Revises: 006b278c0804
Create Date: 2024-11-13 11:57:58.990193

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import UUID

import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '01eb43056184'
down_revision: Union[str, None] = '006b278c0804'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'bg_tasks',
        sa.Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('status', sa.String(500), nullable=False),
        sa.Column('start_datetime', sa.DateTime(), nullable=True, server_default=sa.func.current_timestamp()),
        sa.Column('end_datetime', sa.DateTime(), nullable=True),
        sa.Column('type', sa.String(500), nullable=True),
        sa.Column('percent', sa.String(500), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('bg_tasks')
