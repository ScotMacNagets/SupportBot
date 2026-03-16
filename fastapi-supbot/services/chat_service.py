from sqlalchemy.ext.asyncio import AsyncSession

from .chat_repo import ChatRepository
from .message_repo import MessageRepository


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

        message = await self.message_repo.create_message(
            chat_id=chat.id,
            sender_id=user_id,
            sender_role="user",
            text=text,
        )

        if chat.admin_id:
            await self.manager.send_to_admin(
                admin_id=chat.admin_id,
                chat_id=chat.id,
                text=text
            )
        else:
            admin = await self.chat_repo.assign_free_admin(chat_id=chat.id)

            if admin:
                await self.manager.send_to_admin(
                    admin_id=chat.admin_id,
                    chat_id=chat.id,
                    text=text,
                )
    async def process_admin_message(
            self,
            admin_id: int,
            chat_id: int,
            text: str,
    ):
        chat = await self.chat_repo.get_chat(chat_id)

        await self.message_repo.create_message(
            chat_id=chat.id,
            sender_id=admin_id,
            sender_role="admin",
            text=text,
        )

        await self.manager.send_to_user(
            {
                "type": "message",
                "text": text
            },
            user_id=chat.user_id,
        )