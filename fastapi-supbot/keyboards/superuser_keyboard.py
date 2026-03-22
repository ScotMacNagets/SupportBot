from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.super_user_menu_callback import SuperuserMenuAction, Action, AdminDeleteAction
from core.models import Admin


async def build_superuser_menu_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔑 Выпустить новый ключ",
        callback_data=SuperuserMenuAction(
            action=Action.realise_new_key,
        ).pack()
    )

    builder.button(
        text="⛔ Удалить админа",
        callback_data=SuperuserMenuAction(
            action=Action.admin_delete,
        ).pack()
    )


    return builder.as_markup()

async def build_admin_list(admins: List[Admin]):
    builder = InlineKeyboardBuilder()

    for admin in admins:
        builder.button(
            text=f"Admin:{admin.username} | created_at:{admin.created_at}",
            callback_data=AdminDeleteAction(
                action=Action.admin_delete,
                telegram_id=admin.telegram_id,
            )
        )

    return builder.as_markup()

async def delete_admin_keyboard(telegram_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="⛔ Удалить",
        callback_data=AdminDeleteAction(
            action=Action.confirm_delete,
            telegram_id=telegram_id,
        )
    )

    return builder.as_markup()
