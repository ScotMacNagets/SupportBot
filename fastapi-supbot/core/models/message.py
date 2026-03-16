from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Message(Base):
    sender_id: Mapped[int] = mapped_column(unique=True)
    sender_role: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str]
    sent_at: Mapped[datetime]