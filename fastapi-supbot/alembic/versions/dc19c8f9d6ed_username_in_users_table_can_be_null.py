"""username in users table can be Null

Revision ID: dc19c8f9d6ed
Revises: 99dd46910c53
Create Date: 2026-03-24 11:46:40.759606

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "dc19c8f9d6ed"
down_revision: Union[str, Sequence[str], None] = "99dd46910c53"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users", "username", existing_type=sa.VARCHAR(), nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users", "username", existing_type=sa.VARCHAR(), nullable=False
    )
