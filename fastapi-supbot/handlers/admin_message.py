import logging

from aiogram import Router
from aiogram.types import Message as TelegramMessage
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.connection_manager import manager
from core.models import db_helper, Admin, Message
from services.chat_service import ChatService

router = Router()

logger = logging.getLogger(__name__)

@router.message()
async def admin_reply(
        message: TelegramMessage,
        session: Session,
# @router.message()
# async def admin_reply(
#         message: TelegramMessage,
#         session: AsyncSession,
# ):
#
#     if not message.reply_to_message:
#         await message.reply(
#             text="Ответь реплаем на сообщение пользователя, чтобы отправить ответ в чат."
#         )
#         return
#
#     telegram_message_id = message.reply_to_message.message_id
#
#
#     admin = await session.scalar(
#         select(Admin).where(Admin.telegram_id == message.from_user.id)
#     )
#     if not admin:
#         await message.reply("Ты не зарегистрирован, как админ в системе")
#         return
#
#     src_message = await session.scalar(
#         select(Message).where(Message.telegram_message_id == telegram_message_id)
#     )
#     if not src_message:
#         await message.reply(
#             "Не смог найти, к какому сообщению относится твой ответ. "
#             "Убедись, что отвечаешь именно на сообщение бота с текстом пользователя."
#         )
#         return
#     service = ChatService(
#         session=session,
#         manager=manager,
#     )
#
#     await service.process_admin_message(
#         admin_id=admin.id,
#         chat_id=src_message.chat_id,
#         text=message.text,
#     )

):

    if not message.reply_to_message:
        await message.reply(
            text="Ответь реплаем на сообщение пользователя, чтобы отправить ответ в чат."
        )
        return

    replied_msg_id = message.reply_to_message.message_id

    async for session in db_helper.session_getter():
        admin = await session.scalar(
            select(Admin).where(Admin.telegram_id == message.from_user.id)
        )
        if not admin:
            await message.reply("Ты не зарегистрирован, как админ в системе")
            return

        src_message = await session.scalar(
            select(Message).where(Message.telegram_message_id == replied_msg_id)
        )
        if not src_message:
            await message.reply(
                "Не смог найти, к какому сообщению относится твой ответ. "
                "Убедись, что отвечаешь именно на сообщение бота с текстом пользователя."
            )
            return
        service = ChatService(
            session=session,
            manager=manager,
        )

        await service.process_admin_message(
            admin_id=admin.id,
            chat_id=src_message.chat_id,
            text=message.text,
        )


