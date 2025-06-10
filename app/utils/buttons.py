from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


async def show_buttons_choice(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Управление файловой системой ПК"),
                KeyboardButton(text="Системные действия с ПК"),
                KeyboardButton(text="Логи")
            ]
        ],
        resize_keyboard=True
    )
    msg = await message.answer("Выберите действие: ", reply_markup=keyboard)
    await state.update_data(msg=msg.message_id)


async def show_buttons_file_system(message: Message, state: FSMContext, mode: int = 1):
    keyboard_btns = [
        [
        ]
    ]
    if mode == 2:
        keyboard_btns_to_add = [
            [
                KeyboardButton(text="⬅"),
                KeyboardButton(text="Создать папку/файл в текущей директории"),
                KeyboardButton(text="Удалить папку/файл в текущей директории"),
                KeyboardButton(text="Отправить папку/файл в телеграмм"),
            ]
        ]
        keyboard_btns.extend(keyboard_btns_to_add)
        keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_btns,
            resize_keyboard=True
        )
        await state.update_data(mode=mode)
        await message.answer("Выберите действие: ", reply_markup=keyboard)
    else:
        keyboard_btns_to_add = [
            [
                KeyboardButton(text="⬅"),
                KeyboardButton(text="Сменить текущую директорию"),
                KeyboardButton(text="➡")
            ]
        ]
        keyboard_btns.extend(keyboard_btns_to_add)
        keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_btns,
            resize_keyboard=True
        )
        await state.update_data(mode=mode)
        await message.answer("Выберите действие: ", reply_markup=keyboard)


async def show_buttons_func_file_sys(message: Message, mode: str = "browse"):
    keyboard_btns = [
        [KeyboardButton(text="Назад")]
    ]
    if mode == "delete":
        keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_btns,
            resize_keyboard=True
        )
        await message.answer("Введите цифру файла/папки для удаления", reply_markup=keyboard)
    elif mode == "send":
        keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_btns,
            resize_keyboard=True
        )
        await message.answer("Введите цифру файла/папки для отправки в телеграмм", reply_markup=keyboard)
    elif mode == "create":
        keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_btns,
            resize_keyboard=True
        )
        await message.answer("Введите название папки/файла, но учтите, что если указать просто название, то создаться папка, а если с разрешением, то файл", reply_markup=keyboard)
    else:
        keyboard_btns[0].append(KeyboardButton(text="Вернуться в родительскую директорию"))
        keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_btns,
            resize_keyboard=True
        )
        await message.answer("Введите цифру файла/папки для изменения пути или введите полный путь", reply_markup=keyboard)

async def show_buttons_sys(message: Message, state: FSMContext, mode: int = 1):
    keyboard_btns = [
        [
        ]
    ]
    if mode == 1:
        keyboard_btns_to_add = [
            [
                KeyboardButton(text="⬅"),
                KeyboardButton(text="Пробудить ПК"),
                KeyboardButton(text="Время работы системы"),
                KeyboardButton(text="➡")
            ]
        ]
        keyboard_btns.extend(keyboard_btns_to_add)
        keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_btns,
            resize_keyboard=True
        )
        await message.answer(f"Вы находитесь на {mode} странице \nВыберите действие: ", reply_markup=keyboard)
        await state.update_data(mode=mode)
    elif mode == 2:
        keyboard_btns_to_add = [
            [
                KeyboardButton(text="⬅"),
                KeyboardButton(text="Загрузка CPU, RAM, GPU и т.д."),
                KeyboardButton(text="Посмотреть все процессы"),
                KeyboardButton(text="➡"),
            ]
        ]
        keyboard_btns.extend(keyboard_btns_to_add)
        keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_btns,
            resize_keyboard=True
        )
        await state.update_data(mode=mode)
        await message.answer(f"Вы находитесь на {mode} странице", reply_markup=keyboard)
    elif mode == 3:
        keyboard_btns_to_add = [
            [
                KeyboardButton(text="⬅"),
                KeyboardButton(text="Сделать скриншот"),
                KeyboardButton(text="IP"),
                KeyboardButton(text="➡"),
            ]
        ]
        keyboard_btns.extend(keyboard_btns_to_add)
        keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_btns,
            resize_keyboard=True
        )
        await state.update_data(mode=mode)
        await message.answer(f"Вы находитесь на {mode} странице", reply_markup=keyboard)
    elif mode == 4:
        keyboard_btns_to_add = [
            [
                KeyboardButton(text="⬅"),
                KeyboardButton(text="Выключить ПК"),
                KeyboardButton(text="Перезагрузка ПК"),
            ]
        ]
        keyboard_btns.extend(keyboard_btns_to_add)
        keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_btns,
            resize_keyboard=True
        )
        await state.update_data(mode=mode)
        await message.answer(f"Вы находитесь на {mode} странице", reply_markup=keyboard)

async def show_buttons_shutdown_or_restart(message: Message):
    keyboard_btns = [
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет"),
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard_btns,
        resize_keyboard=True
    )
    await message.answer(f"Вы уверены?", reply_markup=keyboard)