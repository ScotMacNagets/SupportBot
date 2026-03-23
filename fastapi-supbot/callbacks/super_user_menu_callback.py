from enum import Enum

from aiogram.filters.callback_data import CallbackData

from core.config import settings


class SuperuserAction(str, Enum):
    realise_new_key = "realise_new_key"
    admin_list = "admin_list"
    back_to_the_main_menu = "back_to_the_main_menu"

class SuperuserDeleteActions(str, Enum):
    admin_delete = "admin_delete"
    confirm_delete = "confirm_delete"

class SuperuserMenu(CallbackData, prefix=settings.cb.superuser_menu.prefix):
    action: SuperuserAction

class SuperuserAdminDelete(CallbackData, prefix=settings.cb.superuser_admin_delete.prefix):
    action: SuperuserDeleteActions
    telegram_id: int


