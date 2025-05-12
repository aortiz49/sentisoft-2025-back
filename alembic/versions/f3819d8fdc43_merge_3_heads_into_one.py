"""Merge 3 heads into one

Revision ID: f3819d8fdc43
Revises: 3f2f7d19e870, add_question_seed, cd3f1a68c898
Create Date: 2025-05-12 13:58:55.573420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3819d8fdc43'
down_revision: Union[str, None] = ('3f2f7d19e870', 'add_question_seed', 'cd3f1a68c898')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
