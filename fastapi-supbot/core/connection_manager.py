from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

# from core.bot_instance import bot
# from core.models import Message
#
#
# async def send_to_admin(admin_id: int, chat_id: int, text: str):
#
#     message = (
#         f"ChatID: {chat_id}\n\n",
#         f"Message: \n{text}",
#     )
#
#     await bot.send_message(admin_id, message)


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()

        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_to_user(self, user_id: int, data: dict):
        websocket = self.active_connections[user_id]

        if websocket:
            await websocket.send_json(data)

    @staticmethod
    async def send_to_admin(
            admin_id: int,
            chat_id: int,
            text: str,
            session: AsyncSession,
    ):

        message = f"Message: \n\n{text}"

        msg = await bot.send_message(admin_id, message)
        telegram_message_id = msg.message_id

        query = (
            select(Message)
            .where(
                Message.chat_id == chat_id,
                Message.telegram_message_id.is_(None),
            )
            .order_by(Message.id.desc())
        )
        result = await session.execute(query)
        msg_model = result.scalars().first()
        if msg_model:
            msg_model.telegram_message_id = telegram_message_id
            await session.commit()
        




manager = ConnectionManager()