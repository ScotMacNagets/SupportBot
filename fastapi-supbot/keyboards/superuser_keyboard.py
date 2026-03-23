from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.super_user_menu_callback import SuperuserMenu, SuperuserAction, SuperuserAdminDelete, \
    SuperuserDeleteActions
from core.models import Admin
from core.text import AdminSuperuserKeyboard


async def build_superuser_menu_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text=AdminSuperuserKeyboard.REALISE_NEW_KEY,
        callback_data=SuperuserMenu(
            action=SuperuserAction.realise_new_key,
        ).pack()
    )

    builder.button(
        text=AdminSuperuserKeyboard.ADMIN_LIST,
        callback_data=SuperuserMenu(
            action=SuperuserAction.admin_list,
        ).pack()
    )


    return builder.as_markup()

async def build_admin_list(admins: List[Admin]):
    builder = InlineKeyboardBuilder()

    for admin in admins:
        builder.button(
            text=AdminSuperuserKeyboard.ADMIN_BUTTON_FORMAT.format(
                telegram_id=admin.telegram_id,
                username=admin.username,
                created_at=admin.created_at,
            ),
            callback_data=SuperuserAdminDelete(
                action=SuperuserDeleteActions.admin_delete,
                telegram_id=admin.telegram_id,
            ).pack()
        )

    builder.adjust(1)

    return builder.as_markup()

async def delete_admin_keyboard(telegram_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text=AdminSuperuserKeyboard.CONFIRM_DELETE,
        callback_data=SuperuserAdminDelete(
            action=SuperuserDeleteActions.confirm_delete,
            telegram_id=telegram_id,
        ).pack()
    )

    return builder.as_markup()

async def back_to_the_main_menu_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text=AdminSuperuserKeyboard.BACK_TO_THE_MAIN_MENU,
        callback_data=SuperuserAction.back_to_the_main_menu
    )

    return builder.as_markup()
