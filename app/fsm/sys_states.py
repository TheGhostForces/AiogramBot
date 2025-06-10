from aiogram.fsm.state import StatesGroup, State


class SysStates(StatesGroup):
    sys_actions = State()
    shutdown_restart = State()