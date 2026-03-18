from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .chat import Chat


class Message(Base):
    sender_id: Mapped[int] = mapped_column()
    sender_role: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str]
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    telegram_message_id: Mapped[int | None] = mapped_column(unique=True, nullable=True)
    delivered: Mapped[bool] = mapped_column(default=False)

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    chat: Mapped["Chat"] = relationship(back_populates="messages")