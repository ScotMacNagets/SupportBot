import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import router as api_router
from core.config import settings
from core.models import db_helper

logger = logging.getLogger(__name__)

#FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Lifespan events started")
    yield
    await db_helper.dispose()
    logger.info("Lifespan events started")
main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(api_router, prefix=settings.api.prefix)
