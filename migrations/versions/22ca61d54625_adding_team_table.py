"""adding team table

Revision ID: 22ca61d54625
Revises: 7634640a0e6f
Create Date: 2020-03-20 01:00:58.816296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22ca61d54625'
down_revision = '7634640a0e6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team')
    # ### end Alembic commands ###
