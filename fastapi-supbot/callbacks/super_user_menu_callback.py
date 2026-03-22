from enum import Enum

from aiogram.filters.callback_data import CallbackData

from core.config import settings


class Action(str, Enum):
    realise_new_key = "realise_new_key"
    admin_list = "admin_list"
    admin_delete = "admin_delete"
    confirm_delete = "confirm_delete"

class SuperuserMenuAction(CallbackData, prefix="supuser"):
    action: Action

class AdminDeleteAction(CallbackData, prefix="admindelete"):
    action: Action
    telegram_id: str

