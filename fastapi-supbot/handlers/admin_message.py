import logging
from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.types import Message as TelegramMessage, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.admin_message_callback import AdminAction
from core.connection_manager import manager
from core.models import Admin, Message, Chat
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

@router.callback_query(AdminAction.filter(F.action == "answer"))
async def admin_answer(
        query: CallbackQuery,
        callback_data: AdminAction,
        session: AsyncSession,
):
    chat = await session.get(Chat, callback_data.chat_id)
    admin = await session.scalar(
        select(Admin).where(Admin.telegram_id == query.from_user.id)
    )

    if chat.status == "closed":
        await query.answer()
        await query.message.answer(
            text="🗂 Диалог уже закрыт"
        )
        return

    if chat.status == "active":
        await query.answer()
        await query.message.answer(
            text="😒 Ой, уже кто то занял чат",
        )
        return
    await session.commit()

    if admin.current_chat_id:
        await query.answer()
        await query.message.answer(
            "🤔 Сначала заверши свой текущий диалог"
        )
        return

    chat.status = "active"
    chat.admin_id = admin.id

    admin.current_chat_id = chat.id

    await session.commit()

    await query.answer()
    await query.message.answer(
        "✅ Ты принял диалог"
    )

@router.callback_query(AdminAction.filter(F.action == "close"))
async def admin_answer(
        query: CallbackQuery,
        callback_data: AdminAction,
        session: AsyncSession,
):
    chat = await session.get(Chat, callback_data.chat_id)

    admin = await session.scalar(
        select(Admin).where(Admin.telegram_id == query.from_user.id)
    )

    if chat.status == "closed":
        await query.answer()
        await query.message.answer(
            text="🗂 Диалог уже закрыт"
        )

    if admin.current_chat_id != chat.id:
        await query.answer()
        await query.message.answer(
            text="Сначала ✅ прими диалог, а потом нажми кнопку ⛔ закрыть"
        )
        return

    chat.status = "closed"
    chat.closed_at = datetime.now(timezone.utc)

    admin.current_chat_id = None

    await session.commit()

    await query.answer()
    await query.message.answer(
        text="✅ Диалог успешно завершен",
    )

@router.message()
async def admin_answer(
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
            text="⛔ У тебя нет активного диалога"
        )
        return

    chat = await session.get(Chat, admin.current_chat_id)

    if chat.status != "active":
        await message.answer(
            text="🗂 Диалог уже закрыт",
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
