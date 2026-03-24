"""add default to users table

Revision ID: e1892cda59d4
Revises: dc19c8f9d6ed
Create Date: 2026-03-24 11:52:45.280441

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e1892cda59d4"
down_revision: Union[str, Sequence[str], None] = "dc19c8f9d6ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "users",
        "created_at",
        server_default=sa.text("now()"),
        existing_type=sa.DateTime(timezone=True),
        nullable=False
    )

def downgrade():
    op.alter_column(
        "users",
        "created_at",
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        nullable=True
    )
