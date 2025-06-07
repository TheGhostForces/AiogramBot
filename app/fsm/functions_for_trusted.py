from aiogram.fsm.state import StatesGroup, State


class Functions(StatesGroup):
    choosing = State()
    file_system = State()
    delete_content = State()
    change_path = State()
    send_to_tg = State()
    create_folder = State()