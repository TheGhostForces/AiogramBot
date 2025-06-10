from aiogram.fsm.state import StatesGroup, State


class ChooseState(StatesGroup):
    choosing = State()