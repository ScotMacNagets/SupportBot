"""add default to started_at

Revision ID: a27acc8981b3
Revises: 7ad5e8ce8dc0
Create Date: 2026-03-17 10:23:45.883047

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "a27acc8981b3"
down_revision: Union[str, Sequence[str], None] = "7ad5e8ce8dc0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "chats",
        "started_at",
        server_default=sa.text("now()")
    )

def downgrade():
    op.alter_column(
        "chats",
        "started_at",
        server_default=None
    )
