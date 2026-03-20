"""add current_chat_id field into admins table

Revision ID: 4da35a7a9032
Revises: f42d715fada0
Create Date: 2026-03-20 10:39:23.932166

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4da35a7a9032"
down_revision: Union[str, Sequence[str], None] = "f42d715fada0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "admins", sa.Column("current_chat_id", sa.Integer(), nullable=True)
    )
    op.drop_column("admins", "status")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "admins",
        sa.Column("status", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("admins", "current_chat_id")
