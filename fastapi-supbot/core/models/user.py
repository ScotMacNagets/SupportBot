from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base
if TYPE_CHECKING:
    from .chat import Chat


class User(Base):
    username: Mapped[str]
    created_at: Mapped[datetime]

    chats: Mapped[List["Chat"]] = relationship(back_populates="user")