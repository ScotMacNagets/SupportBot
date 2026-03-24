"""create external_id field in users table

Revision ID: 99dd46910c53
Revises: e7c02a423dac
Create Date: 2026-03-24 11:05:36.199863

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "99dd46910c53"
down_revision: Union[str, Sequence[str], None] = "e7c02a423dac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('external_id', sa.String(), nullable=True))

    op.execute("UPDATE users SET external_id = gen_random_uuid()")

    op.alter_column('users', 'external_id', nullable=False)
    op.create_index(
        op.f("ix_users_external_id"), "users", ["external_id"], unique=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_users_external_id"), table_name="users")
    op.drop_column("users", "external_id")
