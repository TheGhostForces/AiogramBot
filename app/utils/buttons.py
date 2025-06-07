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


async def show_buttons_file_system(message: Message, mode: int = 1):
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
        await message.answer("Выберите действие: ", reply_markup=keyboard)
    else:
        keyboard_btns_to_add = [
            [
                KeyboardButton(text="◀️"),
                KeyboardButton(text="Сменить текущую директорию"),
                KeyboardButton(text="➡")
            ]
        ]
        keyboard_btns.extend(keyboard_btns_to_add)
        keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_btns,
            resize_keyboard=True
        )
        await message.answer("Выберите действие: ", reply_markup=keyboard)


async def show_buttons_func(message: Message, state: FSMContext, mode: str = "browse"):
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