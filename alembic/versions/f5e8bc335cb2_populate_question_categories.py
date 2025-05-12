"""add interview question categories

Revision ID: f5e8bc335cb2
Revises: 57739fa245bd
Create Date: 2025-05-12 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = "f5e8bc335cb2"
down_revision = "57739fa245bd"
branch_labels = None
depends_on = None

categories = [
    (
        "Leadership & Decision-Making",
        "Taking initiative, assigning responsibilities, and making strategic choices.",
    ),
    (
        "Mentoring & Growth",
        "Coaching, guiding, or mentoring team members for professional development.",
    ),
    (
        "Feedback & Communication",
        "Giving or receiving feedback, discussing ideas, or resolving misunderstandings.",
    ),
    (
        "Learning & Adaptability",
        "Learning new tools or tech, adapting to changing requirements or environments.",
    ),
    (
        "Agile & Team Practices",
        "Participating in agile ceremonies, sprint planning, or improving team workflows.",
    ),
    (
        "Time & Stress Management",
        "Working under deadlines, avoiding burnout, and managing personal/professional balance.",
    ),
    (
        "Incident & Quality Handling",
        "Handling bugs, production outages, quality assurance, or rollback situations.",
    ),
    (
        "Collaboration & Stakeholders",
        "Working with designers, PMs, analysts, or other departments effectively.",
    ),
]


def upgrade():
    now = datetime.utcnow()
    for category, description in categories:
        stmt = sa.text(
            """
            INSERT INTO question_categories (category, description, created_at, updated_at)
            VALUES (:category, :description, :created_at, :updated_at)
        """
        ).bindparams(
            category=category, description=description, created_at=now, updated_at=now
        )
        op.execute(stmt)


def downgrade():
    for category, _ in categories:
        stmt = sa.text(
            """
            DELETE FROM question_categories
            WHERE category = :category
        """
        ).bindparams(category=category)
        op.execute(stmt)
