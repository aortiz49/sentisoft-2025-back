"""merge question seed and schema branches

Revision ID: 6d8c6d5d59ab
Revises: add_question_seed, cd3f1a68c898
Create Date: 2025-05-11 23:00:42.476758

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6d8c6d5d59ab"
down_revision = ("cd3f1a68c898",)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
