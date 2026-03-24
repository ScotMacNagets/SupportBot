from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
if TYPE_CHECKING:
    from .chat import Chat


class User(Base):
    username: Mapped[str]
    external_id: Mapped[str] = mapped_column(unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    chats: Mapped[List["Chat"]] = relationship(back_populates="user")