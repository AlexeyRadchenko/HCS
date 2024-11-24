"""add year acts file table

Revision ID: 03c93464a0dc
Revises: 02e4878f956e
Create Date: 2024-11-08 13:37:08.731508

"""
from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '03c93464a0dc'
down_revision: Union[str, None] = '02e4878f956e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'yearactfiles',
        sa.Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(500), nullable=False),
        sa.Column('date', sa.Date, nullable=True),
        sa.Column('num', sa.String(100), nullable=True),
        sa.Column('extention', sa.String(500), nullable=False),
        sa.Column('url', sa.String(500), nullable=False),
        sa.Column('path', sa.String(500), nullable=False),
        sa.Column('size', sa.String(500), nullable=True),
        sa.Column('filetype', sa.String(500), nullable=True),
        sa.Column('house_id', sa.Integer(), sa.ForeignKey("houses.id"), nullable=False),
        sa.Column('date_upload', sa.DateTime(), nullable=True, server_default=sa.func.current_timestamp()),
    )


def downgrade() -> None:
    op.drop_table('yearactfiles')
