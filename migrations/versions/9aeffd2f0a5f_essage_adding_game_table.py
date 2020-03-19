"""essage=adding game table

Revision ID: 9aeffd2f0a5f
Revises: fb81504563bf
Create Date: 2020-03-18 23:59:16.992238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9aeffd2f0a5f'
down_revision = 'fb81504563bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'player', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'player', type_='unique')
    # ### end Alembic commands ###
