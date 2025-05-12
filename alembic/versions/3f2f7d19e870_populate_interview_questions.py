"""populate interview questions

Revision ID: 3f2f7d19e870
Revises: 6d8c6d5d59ab
Create Date: 2025-05-11 23:04:43.893768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f2f7d19e870'
down_revision: Union[str, None] = '6d8c6d5d59ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
