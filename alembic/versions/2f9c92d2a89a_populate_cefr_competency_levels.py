"""populate CEFR competency levels

Revision ID: 2f9c92d2a89a
Revises: 57739fa245bd
Create Date: 2025-05-11 22:12:27.028826
"""

from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "2f9c92d2a89a"
down_revision: Union[str, None] = "57739fa245bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

competency_levels_table = sa.table(
    "competency_levels",
    sa.column("competency", sa.String),
    sa.column("description", sa.String),
    sa.column("level", sa.String),
    sa.column("created_at", sa.DateTime),
    sa.column("updated_at", sa.DateTime),
)


competency_levels_data = [
    # Communication
    (
        "communication",
        "Frequent filler words, hesitations, or awkward phrasing that hinder flow.",
        "A1",
    ),
    (
        "communication",
        "Expresses ideas, but language lacks confidence, polish, or appropriate tone.",
        "A2",
    ),
    (
        "communication",
        "Generally fluent and appropriate, though occasionally unclear or imprecise.",
        "B1",
    ),
    (
        "communication",
        "Engages listener with confident tone and dynamic language.",
        "B2",
    ),
    (
        "communication",
        "Fluent, polished delivery with minimal hesitation and good audience awareness.",
        "C1",
    ),
    (
        "communication",
        "Highly articulate, compelling, and audience-aware; conveys ideas with finesse.",
        "C2",
    ),
    # Structure
    ("structure", "Rambling, no clear beginning, middle, or end.", "A1"),
    (
        "structure",
        "Attempts structure but lacks logical flow or proper sequencing.",
        "A2",
    ),
    (
        "structure",
        "Follows a rough format (e.g., STAR) with minor organizational gaps.",
        "B1",
    ),
    (
        "structure",
        "Clear structure with logical transitions and well-ordered content.",
        "B2",
    ),
    ("structure", "Strong transitions, structured argumentation, and pacing.", "C1"),
    (
        "structure",
        "Highly organized, anticipates listener needs, and presents information with precision.",
        "C2",
    ),
    # Clarity
    ("clarity", "Lacks clarity; ideas are vague or ambiguous.", "A1"),
    (
        "clarity",
        "Some ideas are understandable, but message is clouded by poor phrasing.",
        "A2",
    ),
    ("clarity", "Main points are discernible with minor clarification needed.", "B1"),
    ("clarity", "Articulates ideas clearly and avoids ambiguity.", "B2"),
    (
        "clarity",
        "Delivers ideas concisely with consistent clarity and few redundancies.",
        "C1",
    ),
    (
        "clarity",
        "Exceptionally clear, concise, and precise with no room for misunderstanding.",
        "C2",
    ),
]


def upgrade() -> None:
    op.bulk_insert(
        competency_levels_table,
        [
            {
                "competency": competency,
                "description": description,
                "level": level,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            for competency, description, level in competency_levels_data
        ],
    )


def downgrade() -> None:
    for competency, _, level in competency_levels_data:
        op.execute(
            sa.text(
                """
                DELETE FROM competency_levels
                WHERE competency = :competency AND level = :level
            """
            ).bindparams(competency=competency, level=level)
        )
