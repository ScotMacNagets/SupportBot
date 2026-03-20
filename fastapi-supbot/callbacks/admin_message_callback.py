from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Action(str, Enum):
    answer = "answer"
    close = "close"

class AdminAction(CallbackData, prefix="adm"):
    action: Action
    chat_id: int
