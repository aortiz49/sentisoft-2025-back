"""initial_migration

Revision ID: fdc25a369e25
Revises: 641b70fb40cb
Create Date: 2025-05-02 10:42:29.077489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdc25a369e25'
down_revision: Union[str, None] = '641b70fb40cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
