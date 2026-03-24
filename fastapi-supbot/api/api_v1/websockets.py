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
async def ws(websocket: WebSocket):
    async for session in db_helper.session_getter():
        service = ChatService(session, manager)

        user_id = websocket.query_params.get("user_id")

        user = await service.get_or_create_user(user_id=user_id)


        await manager.connect(websocket=websocket, user_id=user.id)
        await service.send_missed_messages(user_id=user.id)


        try:
            while True:
                data = await websocket.receive_json()
                text = data["message"]

                await service.process_user_message(
                    user_id=user.id,
                    text=text,
                )
        except WebSocketDisconnect:
            await manager.disconnect(user.id)

