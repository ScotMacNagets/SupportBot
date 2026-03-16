import logging

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=settings.api.v1.websocket,
    tags=["Websocket"],
)

@router.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            message = data["message"]
            await websocket.send_text(message)
    except WebSocketDisconnect:
        logger.warning("WebSocket disconnected")
