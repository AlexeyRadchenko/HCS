"""create addresses table

Revision ID: 1087208effd6
Revises: 365eb0a0d91a
Create Date: 2022-02-11 13:47:31.764248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1087208effd6'
down_revision = '365eb0a0d91a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'organisations',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('full_name', sa.String(300), nullable=True),
        sa.Column('short_name', sa.String(150), nullable=True)
    )


def downgrade():
    op.drop_table('organisations')


"""def upgrade():
    op.create_table(
        'addresses',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('street', sa.String(50), nullable=True),
        sa.Column('house_number', sa.String(50), nullable=True),
        sa.Column('entrance', sa.String(50), nullable=True),
        sa.Column('appartment', sa.String(50), nullable=True),
        sa.Column('organisation_id', sa.Integer(), sa.ForeignKey('organisations.id'), nullable=True)
    )


def downgrade():
    op.drop_table('addresses')"""
