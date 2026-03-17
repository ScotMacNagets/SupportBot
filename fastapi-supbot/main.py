import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Dispatcher, Router
from fastapi import FastAPI

from api import router as api_router
from bot import start_bot
from core.bot_instance import bot
from core.config import settings
from core.models import db_helper
from main_app import main_app

logger = logging.getLogger(__name__)

async def main():
    config = uvicorn.Config(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=False,
    )

    server = uvicorn.Server(config)

    bot_task = asyncio.create_task(start_bot())
    uvicorn_task = asyncio.create_task(
        server.serve()
    )
    await asyncio.gather(bot_task, uvicorn_task)


if __name__ == '__main__':
    asyncio.run(main())
