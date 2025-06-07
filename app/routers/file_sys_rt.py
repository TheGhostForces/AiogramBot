from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from app.utils import buttons
from app.database.repository import VerifyUser
from app.fsm.functions_for_trusted import Functions
from app.utils.file_sys import current_directory, check_exists_folder, get_folder_content, delete_content_by_number, \
    one_level_up, update_path, change_path_directory, check_absolute_folder, show_content_folder, send_all_types_files, create_folder

router = Router()

@router.message(Functions.file_system)
async def file_system(message: types.Message, state: FSMContext):
    current_path = await current_directory(message)
    if not await check_exists_folder(current_path):
        await VerifyUser.update_path(message.from_user.id, message.from_user.username, "C:/")
        await buttons.show_buttons_file_system(message)
        return await message.answer("Данного пути не существует \nВы были возвращены в C:/")
    if message.text == "Удалить папку/файл в текущей директории":
        await state.set_state(Functions.delete_content)
        await show_content_folder(message)
        await buttons.show_buttons_func(message, state, "delete")
    if message.text == "Сменить текущую директорию":
        await state.set_state(Functions.change_path)
        await show_content_folder(message)
        await buttons.show_buttons_func(message, state)
    if message.text == "Отправить папку/файл в телеграмм":
        await state.set_state(Functions.send_to_tg)
        await show_content_folder(message)
        await buttons.show_buttons_func(message, state, "send")
    if message.text == "Создать папку/файл в текущей директории":
        await state.set_state(Functions.create_folder)
        await show_content_folder(message)
        await buttons.show_buttons_func(message, state, "create")
    if message.text == "➡":
        await message.delete()
        await buttons.show_buttons_file_system(message, 2)
    if message.text == "◀️":
        await message.delete()
        await state.set_state(Functions.choosing)
        await buttons.show_buttons_choice(message, state)
    if message.text == "⬅":
        await message.delete()
        await buttons.show_buttons_file_system(message)

@router.message(Functions.create_folder)
async def create(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        await state.set_state(Functions.file_system)
        await show_content_folder(message)
        await buttons.show_buttons_file_system(message)
    else:
        current_path = await current_directory(message)
        ext = await create_folder(current_path, message.text)
        if ext:
            await show_content_folder(message)
        else:
            await show_content_folder(message)

@router.message(Functions.send_to_tg)
async def send(message: types.Message, state: FSMContext):
    current_path = await current_directory(message)
    content = await get_folder_content(current_path)
    if message.text == "Назад":
        await state.clear()
        await state.set_state(Functions.file_system)
        await show_content_folder(message)
        await buttons.show_buttons_file_system(message)
    else:
        try:
            await send_all_types_files(message, current_path, content, int(message.text))
            await state.clear()
            await state.set_state(Functions.file_system)
            await show_content_folder(message)
            await buttons.show_buttons_file_system(message)
        except ValueError:
            await message.answer("Пожалуйста, введите цифру")
        except KeyError:
            await message.answer("Вы ввели номер, которого нету в списке. Пожалуйста, введите соответствующий номер")
        except PermissionError:
            await message.answer("Похоже, вы выбрали папку/файл, где вам отказали в доступе. Лучше так не делать...")
@router.message(Functions.delete_content)
async def delete(message: types.Message, state: FSMContext):
    current_path = await current_directory(message)
    content = await get_folder_content(current_path)
    if message.text == "Назад":
        await state.clear()
        await state.set_state(Functions.file_system)
        await show_content_folder(message)
        await buttons.show_buttons_file_system(message)
    else:
        try:
            await message.answer(f"Успешно был удален файл по пути: {await delete_content_by_number(current_path, content, int(message.text))}")
            await state.clear()
            await state.set_state(Functions.file_system)
            await show_content_folder(message)
            await buttons.show_buttons_file_system(message)
        except ValueError:
            await message.answer("Пожалуйста, введите цифру")
        except KeyError:
            await message.answer("Вы ввели номер, которого нету в списке. Пожалуйста, введите соответствующий номер")
        except PermissionError:
            await message.answer("Похоже, вы выбрали папку/файл, где вам отказали в доступе. Лучше так не делать...")

@router.message(Functions.change_path)
async def change_path(message: types.Message, state: FSMContext):
    current_path = await current_directory(message)
    if not await check_exists_folder(current_path):
        await VerifyUser.update_path(message.from_user.id, message.from_user.username, "C:/")
        await buttons.show_buttons_file_system(message)
        return await message.answer("Данного пути не существует \nВы были возвращены на C:/")
    content = await get_folder_content(current_path)
    if message.text == "Назад":
        await state.clear()
        await state.set_state(Functions.file_system)
        await show_content_folder(message)
        await buttons.show_buttons_file_system(message)
        return
    if message.text == "Вернуться в родительскую директорию":
        new_path = await one_level_up(current_path)
        await update_path(message, new_path)
        await show_content_folder(message)
        await buttons.show_buttons_func(message, state)
    else:
        try:
            new_path = await change_path_directory(current_path, content, int(message.text))
            if new_path == None:
                await message.answer("Данной директории нету в текущей директории")
                return
            if new_path == "is_file":
                await message.answer("Сюда невозможно переместиться")
                return
            if not new_path[-1] == "/":
                new_path += "/"
            await update_path(message, new_path)
            await show_content_folder(message)
            await buttons.show_buttons_func(message, state)
        except ValueError:
            msg = message.text
            if not msg[-1] == "/":
                msg += "/"
            if await check_absolute_folder(message.text):
                await update_path(message, message.text)
                await show_content_folder(message)
                await buttons.show_buttons_func(message, state)
            else:
                await message.answer("Был введен неправильный путь или его не существует")