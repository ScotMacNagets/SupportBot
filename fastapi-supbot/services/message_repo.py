from core.models import Message


class MessageRepository:

    async def create_message(
            self,
            chat_id: int,
            sender_id: int,
            sender_role:str,
            text: str,
    ):

        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            sender_role=sender_role,
            message=text,
        )

        session.add(message)
        await session.commit()

        return message