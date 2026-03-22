from sqlalchemy import Nullable
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Key(Base):
    hashed_key: Mapped[str] = mapped_column(nullable=False)