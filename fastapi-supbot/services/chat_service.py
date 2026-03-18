import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Chat
from .chat_repo import ChatRepository
from .message_repo import MessageRepository

logger = logging.getLogger(__name__)


class ChatService:

    def __init__(self, session: AsyncSession, manager: ConnectionManager):

        self.session = session
        self.manager = manager

        self.chat_repo = ChatRepository(session)
        self.message_repo = MessageRepository(session)

    async def process_user_message(self, user_id: int, text: str):
        #достаем чат или создаем новый
        chat = await self.chat_repo.get_active_chat(user_id)
        if not chat:
            chat = await self.chat_repo.create_chat(user_id)

        # назначаем админа, если его нет
        admin = chat.admin

        if not admin:
            admin = await self.chat_repo.assign_free_admin(chat_id=chat.id)

        if admin and admin.telegram_id:
            await self._send_to_admin(
                admin_id=admin.telegram_id,
                chat_id=chat.id,
                text=text,
            )

        #сохраняем сообщение в бд
        message = await self.message_repo.create_message(
            sender_id=user_id,
            sender_role="user",
            text=text,
            chat_id=chat.id,
            self_send=True,
        )

        #отправляем пользователю его же сообщение
        payload = {
            "type": "message",
            "message": {
                "id": message.id,
                "chat_id": message.chat_id,
                "sender_id": message.sender_id,
                "sender_role": message.sender_role,
                "text": message.message,
                "created_at": message.sent_at.isoformat(),
            }
        }

        await self.manager.send_to_user(
            user_id=user_id,
            data=payload,
        )




    async def process_admin_message(
            self,
            admin_id: int,
            chat_id: int,
            text: str,
    ):
        #получаем чат, в котором происходит диалог
        chat = await self.chat_repo.get_chat(chat_id)
        if not chat:
            logger.info(f"Chat {chat_id} not found")
            return
        #создаем сообщение и прикрепляем его к чату
        message = await self.message_repo.create_message(
            chat_id=chat.id,
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
        #отправляем сообщение пользователю
            data=payload,
            user_id=chat.user_id,
        )
    async def _send_to_admin(
            self,
            admin_id: int,
            chat_id: int,
            text: str,
    ):
        #формуруем и отправляем сообщение
        message = f"Message: \n\n{text}"

        msg = await bot.send_message(admin_id, message)
        telegram_message_id = msg.message_id

        #записываем id сообщения в бд, чтобы потом определить чат
        query = (
            select(Message)
            .where(
                Message.chat_id == chat_id,
                Message.telegram_message_id.is_(None),
            )
            .order_by(Message.id.desc())
        )
        result = await self.session.execute(query)
        msg_model = result.scalars().first()
        if msg_model:
            msg_model.telegram_message_id = telegram_message_id
            await self.session.commit()