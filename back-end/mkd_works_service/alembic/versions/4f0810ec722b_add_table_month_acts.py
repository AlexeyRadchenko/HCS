"""add table month acts

Revision ID: 4f0810ec722b
Revises: bc0acb3fd0ad
Create Date: 2025-04-11 09:26:11.271392

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '4f0810ec722b'
down_revision: Union[str, None] = 'bc0acb3fd0ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'monthactfiles',
        sa.Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(500), nullable=False),
        sa.Column('date', sa.Date, nullable=True),
        sa.Column('month_year', sa.Date, nullable=True),
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
    op.drop_table('monthactfiles')


def downgrade() -> None:
    pass
