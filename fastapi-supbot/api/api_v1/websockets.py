import logging

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.config import settings
from core.connection_manager import manager
from core.models import db_helper
from services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=settings.api.v1.websocket,
    tags=["Websocket"],
)

@router.websocket("/ws")
async def ws(websocket: WebSocket, user_id: int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            message = data["message"]
            await websocket.send_text(message)
    except WebSocketDisconnect:
        manager.disconnect(user_id)

