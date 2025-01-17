"""empty message

Revision ID: c1bef2046609
Revises: 
Create Date: 2021-11-03 11:13:41.073025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1bef2046609'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Planets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('diameter', sa.String(), nullable=True),
    sa.Column('moons', sa.Boolean(), nullable=True),
    sa.Column('picture', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Planets')
    # ### end Alembic commands ###
