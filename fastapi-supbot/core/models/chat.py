from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
if TYPE_CHECKING:
    from .user import User
    from .message import Message


class Chat(Base):
    started_at: Mapped[datetime]
    closed_at: Mapped[datetime | None]
    status: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    admin_id: Mapped[int] = mapped_column(ForeignKey("admins.id"))

    user: Mapped["User"] = relationship(back_populates="chats")
    admin: Mapped["User"] = relationship(back_populates="admins")
    messages: Mapped[List["Message"]] = relationship(back_populates="chat")