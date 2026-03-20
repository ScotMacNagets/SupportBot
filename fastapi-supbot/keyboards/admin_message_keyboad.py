from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.admin_message_callback import Action, AdminAction



async def answer_keyboard(chat_id: int, first_message: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()


    builder.button(
        text="✅ Принять",
        callback_data=AdminAction(
            action=Action.answer,
            chat_id=chat_id,
        ).pack()
    )

    builder.button(
            text="⛔ Закрыть",
            callback_data=AdminAction(
                action=Action.close,
                chat_id=chat_id,
            ).pack()
        )

    return builder.as_markup()