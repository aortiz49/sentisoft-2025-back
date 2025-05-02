"""make clarity_level, structure_level, and communication_level nullable

Revision ID: 72bc88a34434
Revises: 0a45076e360a
Create Date: 2025-05-02 10:53:56.843966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72bc88a34434'
down_revision: Union[str, None] = '0a45076e360a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
