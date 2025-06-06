"""adds scores to interview

Revision ID: adc6f2c7426a
Revises: ead69153d543
Create Date: 2025-05-13 01:39:44.023789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adc6f2c7426a'
down_revision: Union[str, None] = 'ead69153d543'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('interviews', sa.Column('clarity_score', sa.Integer(), nullable=True))
    op.add_column('interviews', sa.Column('structure_score', sa.Integer(), nullable=True))
    op.add_column('interviews', sa.Column('communication_score', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('interviews', 'communication_score')
    op.drop_column('interviews', 'structure_score')
    op.drop_column('interviews', 'clarity_score')
    # ### end Alembic commands ###
