import logging

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Message, Chat

logger = logging.getLogger(__name__)


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    #Создание сообщения
    async def create_message(
            self,
            chat_id: int,
            sender_id: int,
            sender_role:str,
            text: str,
    ):

        message = Message(
            sender_id=sender_id,
            sender_role=sender_role,
            message=text,
            chat_id=chat_id,
        )

        self.session.add(message)
        await self.session.commit()

        return message

    #получить неотправленные сообщения для пользователя из бд
    async def get_undelivered(self, user_id: int):
        query = (
            select(Message)
            .join(Chat)
            .where(
                Chat.user_id == user_id,
                Chat.status == "active",
                Message.delivered == False,
            )
            .order_by(Message.sent_at)
        )

        result = await self.session.execute(query)
        messages = result.scalars().all()
        return messages


    async def mark_message_delivered(self, message_id: int):
        query = select(Message).where(
            Message.id == message_id,
        )
        result = await self.session.execute(query)
        message = result.scalar_one_or_none()
        if message is None:
            logger.warning(f"Message %s not found", message_id)
            return None


        message.delivered = True
        self.session.add(message)

        await self.session.commit()
        await self.session.refresh(message)

        return message

