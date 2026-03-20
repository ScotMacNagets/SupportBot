import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

import keyboards
from core.bot_instance import bot
from core.connection_manager import ConnectionManager
from core.models import Message, Chat, Admin
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


        #сохраняем сообщение в бд
        message = await self.message_repo.create_message(
            sender_id=user_id,
            sender_role="user",
            text=text,
            chat_id=chat.id,
            self_send=True,
        )


        #Если чат активный, то посылаем админу сообщение
        if chat.status == "active" and chat.admin:
            await self._send_to_admin(
                admin_id=chat.admin.telegram_id,
                chat_id=chat.id,
                text=text,
                first_message = False
            )

        elif chat.status == "new":
            await self._notify_admins_about_new_chat(
                chat_id=chat.id,
                text=text,
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
            sender_id=admin_id,
            sender_role="admin",
            text=text,
            chat_id=chat.id,
        )

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
        #отправляем сообщение пользователю
        delivered = await self.manager.send_to_user(
            data=payload,
            user_id=chat.user_id,
        )

        if delivered:
            await self.message_repo.mark_message_delivered(message_id=message.id)

    async def _notify_admins_about_new_chat(self, chat_id: int, text: str):
        query = select(Admin).where(
            Admin.current_chat_id == None,
        )
        result = await self.session.execute(query)

        admins = result.scalars().all()

        if not admins:
            logger.info("Свободных админов нет")
            return

        for admin in admins:
            await self._send_to_admin(
                admin_id=admin.telegram_id,
                chat_id=chat_id,
                text=text,
            )

    async def _send_to_admin(
            self,
            admin_id: int,
            chat_id: int,
            text: str,
    ):
        #формуруем и отправляем сообщение
        message = f"Новое сообщение от пользователя: \n\n{text}"

        msg = await bot.send_message(
            chat_id=admin_id,
            text=message,
            reply_markup=await keyboards.answer_keyboard(
                chat_id=chat_id,
                first_message=first_message,
            ),
        )
        telegram_message_id = msg.message_id

        #записываем id сообщения в бд для дебага и статистики
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


    async def send_missed_messages(self, user_id: int):
        #достаем сообщения, которые не были отправлены
        messages = await self.message_repo.get_undelivered(user_id)

        #получаем соединение для пользователя
        websocket = self.manager.get_active_connections(user_id=user_id)
        if not websocket:
            logger.info(f"No active connections for {user_id}")
            return
        #отправляем сообщения
        for message in messages:
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
            #отправляем сообщение
            sent = await self.manager.send_to_user(
                user_id=user_id,
                data=payload,
            )
            # помечаем сообщения, как доставленные
            await self.message_repo.mark_message_delivered(message_id=message.id)

