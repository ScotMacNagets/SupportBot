from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
if TYPE_CHECKING:
    from .chat import Chat


class Admin(Base):
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime]
    status: Mapped[str] = mapped_column(default='free')

    chats: Mapped[List["Chat"]] = relationship(back_populates="admins")