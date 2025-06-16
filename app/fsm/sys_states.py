from aiogram.fsm.state import StatesGroup, State


class SysStates(StatesGroup):
    sys_actions = State()
    kill_process = State()
    shutdown_restart = State()