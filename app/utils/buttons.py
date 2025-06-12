from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def inline_buttons_choose():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Управление файловой системой ПК", callback_data="Файловая система")],
        [InlineKeyboardButton(text="Системные действия с ПК", callback_data="Системные действия")],
        [InlineKeyboardButton(text="Логи", callback_data="Логи")],
    ])
    return keyboard

async def inline_buttons_file_sys():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить папку/файл в текущей директории", callback_data="Удалить")],
        [InlineKeyboardButton(text="Сменить текущую директорию", callback_data="Сменить")],
        [InlineKeyboardButton(text="Отправить папку/файл в телеграмм", callback_data="Отправить")],
        [InlineKeyboardButton(text="Создать папку/файл в текущей директории", callback_data="Создать")],
        [InlineKeyboardButton(text="Назад", callback_data="Назад в главное меню")],
    ])
    return keyboard

async def inline_button_back():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="Назад в функции файловой системы")],
    ])
    return keyboard

async def inline_buttons_change_directory():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в родительскую директорию", callback_data="В родительскую директорию")],
        [InlineKeyboardButton(text="Назад", callback_data="Назад в функции файловой системы")],
    ])
    return keyboard

async def inline_buttons_sys():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пробудить ПК", callback_data="Пробудить"), InlineKeyboardButton(text="Время работы", callback_data="Время")],
        [InlineKeyboardButton(text="Загрузка CPU, RAM и т.д.", callback_data="Загрузка"), InlineKeyboardButton(text="Все процессы", callback_data="Все процессы")],
        [InlineKeyboardButton(text="Скриншот", callback_data="Скриншот")],
        [InlineKeyboardButton(text="Выключить ПК", callback_data="Выключить"), InlineKeyboardButton(text="Перезагрузка ПК", callback_data="Перезагрузка")],
        [InlineKeyboardButton(text="Назад", callback_data="Назад в главное меню")],
    ])
    return keyboard

async def inline_buttons_yes_no():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="Да"), InlineKeyboardButton(text="Нет", callback_data="Нет")],
    ])
    return keyboard