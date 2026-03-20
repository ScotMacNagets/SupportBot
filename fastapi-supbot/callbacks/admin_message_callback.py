from enum import Enum

from aiogram.filters.callback_data import CallbackData

from core.config import settings


class Action(str, Enum):
    answer = "answer"
    close = "close"

class AdminAction(CallbackData, prefix=settings.cb.admin_action.prefix):
    action: Action
    chat_id: int
