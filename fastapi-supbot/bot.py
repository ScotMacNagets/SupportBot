import asyncio
import logging

from aiogram import Dispatcher

from core.bot_instance import bot
from core.models import db_helper
from handlers import admin_message_router, admin_register_router, superuser_menu_router
from middleware import DBMiddleware

logger = logging.getLogger(__name__)

#Bot
dp = Dispatcher()
dp.include_router(admin_register_router)
dp.include_router(superuser_menu_router)
dp.include_router(admin_message_router)

dp.update.middleware(
        DBMiddleware(
            db=db_helper
        )
    )

async def start_bot():
    try:
        await dp.start_polling(
            bot,
            skip_updates=True,
        )
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Got stop signal. Shutting down...")
    except Exception as error:
        logger.critical(
            "Critical error while bot working: %s",
            error,
            exc_info=True,
        )
    finally:
        await bot.session.close()
        logger.info("Bot session closed.")