from fastapi import APIRouter

from core.config import settings

from .websockets import router as websocket_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(websocket_router)