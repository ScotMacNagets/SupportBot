"""create key table and add is_superuser_field in admin table

Revision ID: e7c02a423dac
Revises: 4da35a7a9032
Create Date: 2026-03-22 15:52:15.890299

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e7c02a423dac"
down_revision: Union[str, Sequence[str], None] = "4da35a7a9032"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "keys",
        sa.Column("hashed_key", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "admins", sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default=sa.text("false"))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("admins", "is_superuser")
    op.drop_table("keys")
