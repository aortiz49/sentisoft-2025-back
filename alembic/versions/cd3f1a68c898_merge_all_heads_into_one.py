"""merge all heads into one

Revision ID: cd3f1a68c898
Revises: 2f9c92d2a89a, f5e8bc335cb2, fdc25a369e25
Create Date: 2025-05-11 22:31:59.095314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd3f1a68c898'
down_revision: Union[str, None] = ('2f9c92d2a89a', 'f5e8bc335cb2', 'fdc25a369e25')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
