"""add column delivered in messages table

Revision ID: f42d715fada0
Revises: ee4537a1b733
Create Date: 2026-03-18 13:14:30.417251

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f42d715fada0"
down_revision: Union[str, Sequence[str], None] = "ee4537a1b733"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "messages", sa.Column(
            "delivered",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("messages", "delivered")
