"""initial_migration

Revision ID: 641b70fb40cb
Revises: fc1358c443f1
Create Date: 2025-05-02 10:40:14.536065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '641b70fb40cb'
down_revision: Union[str, None] = 'fc1358c443f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
