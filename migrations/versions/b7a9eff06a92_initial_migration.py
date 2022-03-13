"""Initial migration.

Revision ID: b7a9eff06a92
Revises: 
Create Date: 2022-03-12 18:36:19.265021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7a9eff06a92'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('guessing_game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('passcode_hash', sa.String(length=256), nullable=True),
    sa.Column('catch_phrase', sa.String(length=512), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('guessing_game')
    # ### end Alembic commands ###