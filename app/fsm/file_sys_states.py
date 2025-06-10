from aiogram.fsm.state import StatesGroup, State


class FileSysStates(StatesGroup):
    file_system = State()
    delete_content = State()
    change_path = State()
    send_to_tg = State()
    create_folder = State()