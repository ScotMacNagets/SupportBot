from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    input_key = State()