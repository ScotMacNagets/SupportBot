from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Message


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

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