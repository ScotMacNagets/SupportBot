from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Chat, Admin


class ChatRepository:
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def get_active_chat(
            self,
            user_id: int,
    ):

        query = select(Chat).where(
            Chat.user_id == user_id,
            Chat.status == "active"
        )

        result = await self.session.execute(query)

        active_chat = result.scalar_one_or_none()

        if active_chat:
            return active_chat
        return None

    async def create_chat(self, user_id: int):

        chat = Chat(
            user_id=user_id,
            status="active",
        )

        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)

        return chat

    async def get_chat(
            self,
            chat_id: int,
    ):
        query = select(Chat).where(
            Chat.id == chat_id,
        )
        result = await self.session.execute(query)

        chat = result.scalar_one_or_none()
        return chat

    async def assign_free_admin(
            self,
            chat_id:int,
    ) -> Admin:
        query = select(Admin).where(
            Admin.status == "free"
        )

        result = await self.session.execute(query)

        admin = result.scalars().first()

        if not admin:
            return None

        admin.status = "busy"

        chat = await self.session.get(Chat, chat_id)
        chat.admin_id = admin.id

        await self.session.commit()

        return admin

