"""init tables create

Revision ID: 9a1d8cacf8f4
Revises: 
Create Date: 2024-10-18 08:34:31.349048

"""
from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '9a1d8cacf8f4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('full_name', sa.String(500), nullable=False),
        sa.Column('short_name', sa.String(500), nullable=False),
        sa.Column('dirname', sa.String(500), nullable=True),
        sa.Column('dirsurname', sa.String(500), nullable=True),
        sa.Column('dirsecondname', sa.String(500), nullable=True),
    )

    op.create_table(
        'houses',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('street', sa.String(500), nullable=False),
        sa.Column('number', sa.String(500), nullable=False),
        sa.Column('company_id', sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column('director', sa.String(500), nullable=True),
        sa.Column('director_appartment', sa.String(500), nullable=True),
    )

    op.create_table(
        'mainworks',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('work', sa.String(), nullable=False),
        sa.Column('workType', sa.String(50), nullable=False),
        sa.Column('companyWorkType', sa.String(50), nullable=False),
    )

    op.create_table(
        'subworks',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('work', sa.String(), nullable=False),
        sa.Column('workType', sa.String(50), nullable=False),
        sa.Column('period', sa.String(100), nullable=False),
        sa.Column('base', sa.String(500), nullable=False),
        sa.Column('companyWorkType', sa.String(50), nullable=False),
        sa.Column('mainwork_id', sa.Integer(), sa.ForeignKey("mainworks.id"), nullable=False),
    )

    op.create_table(
        'fixworks',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('work', sa.String(), nullable=False),
        sa.Column('workType', sa.String(50), nullable=False),
        sa.Column('period', sa.String(100), nullable=False),
        sa.Column('base', sa.String(500), nullable=False),
        sa.Column('companyWorkType', sa.String(50), nullable=False),
        sa.Column('mainwork_id', sa.Integer(), sa.ForeignKey("mainworks.id"), nullable=False),
    )


    op.create_table(
        'actfiles',
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
    )

    op.create_table(
        'smetafiles',
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
    )

    op.create_table(
        'techfiles',
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
    )

    op.create_table(
        'acts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('date', sa.Date, nullable=True),
        sa.Column('start_date', sa.Date, nullable=True),
        sa.Column('end_date', sa.Date, nullable=True),
        sa.Column('num', sa.String(100), nullable=True),
        sa.Column('house_id', sa.Integer(), sa.ForeignKey("houses.id"), nullable=False),
        sa.Column('all_sum', sa.String(500), nullable=False),
    )

    op.create_table(
        'actshasactfiles',
        sa.Column('act_id', sa.Integer(), sa.ForeignKey("acts.id"), primary_key=True),
        sa.Column('actfile_uuid', UUID(as_uuid=True), sa.ForeignKey("actfiles.uuid"), primary_key=True),
    )

    op.create_table(
        'actshassmetafiles',
        sa.Column('act_id', sa.Integer(), sa.ForeignKey("acts.id"), primary_key=True),
        sa.Column('smetafile_uuid', UUID(as_uuid=True), sa.ForeignKey("smetafiles.uuid"), primary_key=True),
    )

    op.create_table(
        'acthasmainworks',
        sa.Column('act_id', sa.Integer(), sa.ForeignKey("acts.id"), primary_key=True),
        sa.Column('mainwork_id', sa.Integer(), sa.ForeignKey("mainworks.id"), primary_key=True),
        sa.Column('sum', sa.String(300), nullable=True),
        sa.Column('quantity', sa.String(500), nullable=True),
        sa.Column('unitcost', sa.String(500), nullable=True),
    )

    op.create_table(
        'acthassubworks',
        sa.Column('act_id', sa.Integer(), sa.ForeignKey("acts.id"), primary_key=True),
        sa.Column('subwork_id', sa.Integer(), sa.ForeignKey("subworks.id"), primary_key=True),
        sa.Column('sum', sa.String(300), nullable=True),
        sa.Column('quantity', sa.String(500), nullable=True),
        sa.Column('unitcost', sa.String(500), nullable=True),
    )

    op.create_table(
        'acthasfixworks',
        sa.Column('act_id', sa.Integer(), sa.ForeignKey("acts.id"), primary_key=True),
        sa.Column('fixwork_id', sa.Integer(), sa.ForeignKey("fixworks.id"), primary_key=True),
        sa.Column('sum', sa.String(300), nullable=True),
        sa.Column('quantity', sa.String(500), nullable=True),
        sa.Column('unitcost', sa.String(500), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('companies')
    op.drop_table('houses')
    op.drop_table('mainworks')
    op.drop_table('subworks')
    op.drop_table('fixworks')
    op.drop_table('actfiles')
    op.drop_table('smetafiles')
    op.drop_table('techfiles')
    op.drop_table('acts')
    op.drop_table('actshasactfiles')
    op.drop_table('actshassmetafiles')
    op.drop_table('acthasmainworks')
    op.drop_table('acthassubworks')
    op.drop_table('acthasfixworks')
