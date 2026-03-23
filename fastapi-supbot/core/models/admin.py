from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
if TYPE_CHECKING:
    from .chat import Chat


class Admin(Base):
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    is_superuser: Mapped[bool] = mapped_column(default=False)
    # status: Mapped[str] = mapped_column(default='free')
    current_chat_id: Mapped[int | None]
    chats: Mapped[List["Chat"]] = relationship(back_populates="admin")