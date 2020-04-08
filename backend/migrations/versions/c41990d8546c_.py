"""empty message

Revision ID: c41990d8546c
Revises: 
Create Date: 2020-01-16 18:18:56.033644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c41990d8546c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('u_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('sex', sa.String(length=2), nullable=True),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('mail', sa.String(length=64), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('pwd', sa.String(length=512), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('u_users')
    # ### end Alembic commands ###
