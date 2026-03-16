from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .chat import Chat


class Message(Base):
    sender_id: Mapped[int] = mapped_column(unique=True)
    sender_role: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str]
    sent_at: Mapped[datetime]

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    chat: Mapped["Chat"] = relationship(back_populates="messages")