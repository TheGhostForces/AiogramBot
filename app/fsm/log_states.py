from aiogram.fsm.state import StatesGroup, State


class LogStates(StatesGroup):
    choice_log = State()
    system_log = State()
    bot_log = State()