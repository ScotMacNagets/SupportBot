import logging
from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.types import Message as TelegramMessage, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.admin_message_callback import AdminAction, Action
from core.config import settings
from core.connection_manager import manager
from core.models import Admin, Message, Chat
from core.text import AdminMessage
from services.chat_service import ChatService

router = Router()

logger = logging.getLogger(__name__)

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

async def _get_admin(session: AsyncSession, telegram_id: int) -> Admin | None:
    return await session.scalar(select(Admin).where(Admin.telegram_id == telegram_id))

async def _answer_query(query, text: str):
    await query.answer()
    await query.message.answer(text=text)

@router.callback_query(AdminAction.filter(F.action == Action.answer))
async def admin_answer(
        query: CallbackQuery,
        callback_data: AdminAction,
        session: AsyncSession,
):
    chat = await session.get(Chat, callback_data.chat_id)
    admin = await _get_admin(
        session=session,
        telegram_id=query.from_user.id,
    )

    if chat.status == settings.chat_states.closed:
        await _answer_query(
            query=query,
            text=AdminMessage.ALREADY_CLOSED,
        )
        return

    if chat.status == settings.chat_states.active:
        await _answer_query(
            query=query,
            text=AdminMessage.ALREADY_TOOK,
        )
        return

    await session.commit()

    if admin.current_chat_id:
        await _answer_query(
            query=query,
            text=AdminMessage.CLOSE_YOUR_CURRENT_CHAT,
        )
        return

    chat.status = settings.chat_states.active
    chat.admin_id = admin.id

    admin.current_chat_id = chat.id

    await session.commit()

    await query.answer()
    await query.message.answer(
        text=AdminMessage.ACCEPTED_CHAT
    )

    service = ChatService(
        session=session,
        manager=manager,
    )

    await service.process_admin_message(
        admin_id=admin.id,
        chat_id=chat.id,
        text=AdminMessage.ADMIN_IS_GONNA_ANSWER_YOU,
    )

@router.callback_query(AdminAction.filter(F.action == Action.close))
async def admin_answer(
        query: CallbackQuery,
        callback_data: AdminAction,
        session: AsyncSession,
):
    chat = await session.get(Chat, callback_data.chat_id)

    admin = await _get_admin(
        session=session,
        telegram_id=query.from_user.id,
    )

    if chat.status == settings.chat_states.closed:
        await _answer_query(
            query=query,
            text=AdminMessage.ALREADY_CLOSED,
        )
        return

    if admin.current_chat_id != chat.id:
        await _answer_query(
            query=query,
            text=AdminMessage.ACCEPT_THEN_CLOSE,
        )
        return

    chat.status = settings.chat_states.closed
    chat.closed_at = datetime.now(timezone.utc)

    admin.current_chat_id = None

    await session.commit()

    await query.answer()
    await query.message.answer(
        text=AdminMessage.SUCCESSFULLY_CLOSED,
    )

    service = ChatService(
        session=session,
        manager=manager,
    )

    await service.process_admin_message(
        admin_id=admin.id,
        chat_id=chat.id,
        text=AdminMessage.ADMIN_CLOSED_DIALOG,
    )

@router.message()
async def admin_message_handler(
        message: TelegramMessage,
        session: AsyncSession,
):
    admin = await session.scalar(
        select(Admin).where(Admin.telegram_id == message.from_user.id)
    )

    if not admin:
        return

    if not admin.current_chat_id:
        await message.answer(
            text=AdminMessage.DONT_HAVE_ACTIVE_CHAT
        )
        return

    chat = await session.get(Chat, admin.current_chat_id)

    if chat.status != settings.chat_states.active:
        await message.answer(
            text=AdminMessage.ALREADY_CLOSED,
        )
        return

    service = ChatService(
        session=session,
        manager=manager,
    )

    await service.process_admin_message(
        admin_id=admin.id,
        chat_id=chat.id,
        text=message.text,
    )
