import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Chat
from .chat_repo import ChatRepository
from .message_repo import MessageRepository

logger = logging.getLogger(__name__)


class ChatService:

    def __init__(self, session: AsyncSession, manager):

        self.session = session
        self.manager = manager

        self.chat_repo = ChatRepository(session)
        self.message_repo = MessageRepository(session)

    async def process_user_message(self, user_id: int, text: str):
        chat = await self.chat_repo.get_active_chat(user_id)
        if not chat:
            chat = await self.chat_repo.create_chat(user_id)

        await self.message_repo.create_message(
            sender_id=user_id,
            sender_role="user",
            text=text,
            chat_id=chat.id,
        )

        chat = await self.session.execute(
            select(Chat)
            .options(selectinload(Chat.admin))  # сразу подгружаем admin
            .where(Chat.status == "active", Chat.user_id == user_id)
        )
        chat = chat.scalars().first()

        admin = chat.admin

        if not admin:
            admin = await self.chat_repo.assign_free_admin(chat_id=chat.id)

        if admin and admin.telegram_id:
            await self.manager.send_to_admin(
                admin_id=admin.telegram_id,
                chat_id=chat.id,
                text=text,
                session=self.session,
            )


    async def process_admin_message(
            self,
            admin_id: int,
            chat_id: int,
            text: str,
    ):
        chat = await self.chat_repo.get_chat(chat_id)
        if not chat:
            logger.info(f"Chat {chat_id} not found")
            return

        message = await self.message_repo.create_message(
            chat_id=chat.id,
            sender_id=admin_id,
            sender_role="admin",
            text=text,
        )

        payload = {
            "type": "message",
            "message": {
                "id": message.id,
                "chat_id": chat.id,
                "sender_id": message.sender_id,
                "sender_role": message.sender_role,
                "text": message.message,
                "created_at": message.sent_at.isoformat(),
            }
        }

        await self.manager.send_to_user(
            data=payload,
            user_id=chat.user_id,
        )