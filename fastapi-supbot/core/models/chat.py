from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
if TYPE_CHECKING:
    from .user import User
    from .message import Message
    from .admin import Admin


class Chat(Base):
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id"))

    user: Mapped["User"] = relationship(back_populates="chats")
    admin: Mapped["Admin"] = relationship(back_populates="chats")
    messages: Mapped[List["Message"]] = relationship(back_populates="chat")