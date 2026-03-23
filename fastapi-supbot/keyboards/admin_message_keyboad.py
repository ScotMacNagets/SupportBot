from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.admin_message_callback import Action, AdminAction
from core.text import AdminMessageKeyboard


async def answer_keyboard(chat_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=AdminMessageKeyboard.ACCEPT,
        callback_data=AdminAction(
            action=Action.answer,
            chat_id=chat_id,
        ).pack()

    )

    builder.button(
        text=AdminMessageKeyboard.CLOSE,
        callback_data=AdminAction(
            action=Action.close,
            chat_id=chat_id,
        ).pack()
    )

    return builder.as_markup()