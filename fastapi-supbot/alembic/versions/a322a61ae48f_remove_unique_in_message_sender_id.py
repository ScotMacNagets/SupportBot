"""remove unique in message sender_id

Revision ID: a322a61ae48f
Revises: f6f288aba0d1
Create Date: 2026-03-17 11:36:38.194516

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "a322a61ae48f"
down_revision: Union[str, Sequence[str], None] = "f6f288aba0d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        op.f("messages_sender_id_key"), "messages", type_="unique"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint(
        op.f("messages_sender_id_key"),
        "messages",
        ["sender_id"],
        postgresql_nulls_not_distinct=False,
    )
