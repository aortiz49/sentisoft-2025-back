"""initial_migration

Revision ID: 0a45076e360a
Revises: fdc25a369e25
Create Date: 2025-05-02 10:46:31.582744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a45076e360a'
down_revision: Union[str, None] = 'fdc25a369e25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
