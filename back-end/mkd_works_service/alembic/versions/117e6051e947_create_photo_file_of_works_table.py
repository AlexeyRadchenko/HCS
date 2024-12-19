"""create photo file of works table

Revision ID: 117e6051e947
Revises: 01eb43056184
Create Date: 2024-11-20 12:56:23.860983

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import UUID

import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '117e6051e947'
down_revision: Union[str, None] = '01eb43056184'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'photofilesdoneworks',
        sa.Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(500), nullable=False),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('date', sa.Date, nullable=True),
        sa.Column('num', sa.String(100), nullable=True),
        sa.Column('extention', sa.String(500), nullable=False),
        sa.Column('url', sa.String(500), nullable=True),
        sa.Column('path', sa.String(500), nullable=False),
        sa.Column('size', sa.String(500), nullable=True),
        sa.Column('filetype', sa.String(500), nullable=True),
        sa.Column('date_upload', sa.DateTime(), nullable=True, server_default=sa.func.current_timestamp()),
        sa.Column('house_id', sa.Integer(), sa.ForeignKey("houses.id"), nullable=False),
        sa.Column('act_id', sa.Integer(), sa.ForeignKey("acts.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('photofilesdoneworks')
