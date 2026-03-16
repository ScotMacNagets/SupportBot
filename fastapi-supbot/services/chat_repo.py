from sqlalchemy import select

from core.models import Chat, Admin


class ChatRepository:

    async def get_active_chat(self, user_id: int):

        query = select(Chat).where(
            Chat.user_id == user_id,
            Chat.status == "active"
        )

        result = await session.execute(query)

        active_chat = result.scalar_one_or_none()

        return active_chat

    async def create_chat(self, user_id: int):

        chat = Chat(
            user_id=user_id,
            status="active",
        )

        session.add(chat)
        await session.commit()
        await session.refresh(chat)

        return chat

    async def assign_free_admin(self, chat_id: int):
        query = select(Admin).where(
            Admin.status == "free"
        )

        result = await session.execute(query)

        admin = result.scalars().first()

        if not admin:
            return None

        admin.status = "busy"

        chat = await session.get(Chat, chat_id)
        chat.admin_id = admin.id

        await session.commit()

        return admin

