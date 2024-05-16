"""empty message

Revision ID: 109e0089e2b1
Revises: f65ea8f8375e
Create Date: 2024-05-15 09:20:50.053576

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '109e0089e2b1'
down_revision: Union[str, None] = 'f65ea8f8375e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_groups',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('group_name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['group_name'], ['groups.group_name'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'group_name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_groups')
    # ### end Alembic commands ###
