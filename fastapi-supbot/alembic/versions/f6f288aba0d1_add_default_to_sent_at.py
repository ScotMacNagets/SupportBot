"""add default to sent_at

Revision ID: f6f288aba0d1
Revises: a27acc8981b3
Create Date: 2026-03-17 11:13:50.613818

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f6f288aba0d1"
down_revision: Union[str, Sequence[str], None] = "a27acc8981b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "messages",
        "sent_at",
        server_default=sa.text("now()"),
        existing_type=sa.DateTime(timezone=True),
        nullable=False
    )

def downgrade():
    op.alter_column(
        "messages",
        "sent_at",
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        nullable=True
    )
