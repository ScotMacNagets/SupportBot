import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.bot_instance import bot
from core.models import Message

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}


    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()

        self.active_connections[user_id] = websocket



    async def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]


    def get_active_connections(self, user_id: int):
        websocket = self.active_connections.get(user_id)
        if not websocket:
            return False
        return websocket


    async def send_to_user(self, user_id: int, data: dict) -> bool:
        websocket = self.active_connections.get(user_id)

        if not websocket:
            logger.info("User %s has no active connection", user_id)
            return False

        try:
            await websocket.send_json(data)
            return True
        except (WebSocketDisconnect, RuntimeError) as e:
            logger.warning(f"Failed to send message to %s: %s", user_id, e)
            return False


manager = ConnectionManager()