import asyncio
import logging

import uvicorn

from bot import start_bot
from core.config import settings

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
