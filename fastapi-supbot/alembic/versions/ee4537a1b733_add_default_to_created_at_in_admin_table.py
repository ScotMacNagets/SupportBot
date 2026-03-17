"""add default to created_at in admin table

Revision ID: ee4537a1b733
Revises: a322a61ae48f
Create Date: 2026-03-17 11:39:47.642080

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ee4537a1b733"
down_revision: Union[str, Sequence[str], None] = "a322a61ae48f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "admins",
        "created_at",
        server_default=sa.text("now()"),
        existing_type=sa.DateTime(timezone=True),
        nullable=False
    )

def downgrade():
    op.alter_column(
        "admins",
        "created_at",
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        nullable=True
    )
