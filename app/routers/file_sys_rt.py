import asyncio
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from app.database.enums import LogsAction
from app.database.repository import History
from app.utils import buttons
from app.fsm.file_sys_states import FileSysStates
from app.utils.file_sys import current_directory, get_folder_content, delete_content_by_number, \
    one_level_up, update_path, change_path_directory, check_absolute_folder, show_content_folder, send_all_types_files, create_folder


router = Router()


@router.callback_query(F.data == "Назад в функции файловой системы")
async def back_to_file_sys(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.BACK_TO_FILE_SYSTEM,
        True,
        {
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await state.set_state(FileSysStates.file_system)
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text=await show_content_folder(data.get("main_message")),
        reply_markup= await buttons.inline_buttons_file_sys()
    )

@router.callback_query(FileSysStates.file_system, F.data == "Удалить")
async def delete_path_file(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.DELETE_MENU,
        True,
        {
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await state.set_state(FileSysStates.delete_content)
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text=await show_content_folder(data.get("main_message")) + f"\n\nВведите цифру папки/файла для удаления",
        reply_markup= await buttons.inline_button_back()
    )

@router.callback_query(FileSysStates.file_system, F.data == "Сменить")
async def change_path(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.CHANGE_MENU,
        True,
        {
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await state.set_state(FileSysStates.change_path)
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text=await show_content_folder(data.get("main_message")) + f"\n\nВведите цифру папки/файла, в которую вы хотите переместиться",
        reply_markup= await buttons.inline_buttons_change_directory()
    )

@router.callback_query(FileSysStates.file_system, F.data == "Отправить")
async def send_file(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.SEND_MENU,
        True,
        {
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await state.set_state(FileSysStates.send_to_tg)
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text=await show_content_folder(data.get("main_message")) + f"\n\nВведите цифру папки/файла, которую вы хотите отправить сюда",
        reply_markup= await buttons.inline_button_back()
    )

@router.callback_query(FileSysStates.file_system, F.data == "Создать")
async def create_folder_file(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.CREATE_MENU,
        True,
        {
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await state.set_state(FileSysStates.create_folder)
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text=await show_content_folder(data.get("main_message")) + f"\n\nВведите название папки/файла, но учтите, если название будет без расширения, то создаться папка",
        reply_markup= await buttons.inline_button_back()
    )

@router.message(FileSysStates.delete_content)
async def delete(message: types.Message, state: FSMContext):
    current_path = await current_directory(message)
    content = await get_folder_content(current_path)
    data = await state.get_data()
    try:
        path = await delete_content_by_number(current_path, content, int(message.text))
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.DELETE,
            True,
            {
                "path": current_path,
                "path_to_delete": str(path),
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await message.delete()
        await message.bot.edit_message_text(
            chat_id=data.get("msg_chat_id"),
            message_id=data.get("msg_id"),
            text=await show_content_folder(data.get("main_message")) + f"\n\nВведите цифру папки/файла для удаления",
            reply_markup=await buttons.inline_button_back()
        )
        err_msg = await message.answer(f"Успешно была удалена папка/файл по пути: {path}")
        await asyncio.sleep(3)
        await err_msg.delete()
    except ValueError:
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.DELETE,
            False,
            {
                "path": current_path,
                "message": message.text,
                "error": "ValueError",
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await message.delete()
        err_msg = await message.answer("Пожалуйста, введите цифру")
        await asyncio.sleep(3)
        await err_msg.delete()
    except KeyError:
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.DELETE,
            False,
            {
                "path": current_path,
                "message": message.text,
                "error": "KeyError",
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await message.delete()
        err_msg = await message.answer("Вы ввели номер, которого нету в списке. Пожалуйста, введите соответствующий номер")
        await asyncio.sleep(3)
        await err_msg.delete()
    except PermissionError:
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.DELETE,
            False,
            {
                "path": current_path,
                "message": message.text,
                "error": "PermissionError",
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await message.delete()
        err_msg = await message.answer("Похоже, вы выбрали папку/файл, где вам отказали в доступе. Лучше так не делать...")
        await asyncio.sleep(3)
        await err_msg.delete()

@router.message(FileSysStates.create_folder)
async def create(message: types.Message, state: FSMContext):
    current_path = await current_directory(message)
    data = await state.get_data()
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.CREATE,
        True,
        {
            "path": current_path,
            "new_folder_file": current_path + message.text,
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await create_folder(current_path, message.text)
    await message.delete()
    await message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text=await show_content_folder(data.get("main_message")) + f"\n\nВведите название папки/файла, но учтите, если название будет без расширения, то создаться папка",
        reply_markup=await buttons.inline_button_back()
    )
    err_msg = await message.answer(f"Успешно была создана папка/файл по пути: {current_path + message.text}")
    await asyncio.sleep(3)
    await err_msg.delete()

@router.message(FileSysStates.send_to_tg)
async def send_file_folder(message: types.Message, state: FSMContext):
    current_path = await current_directory(message)
    content = await get_folder_content(current_path)
    data = await state.get_data()
    try:
        text = await send_all_types_files(message, current_path, content, int(message.text))
        if text:
            err_msg = await message.answer(text)
            await asyncio.sleep(3)
            await err_msg.delete()
        await message.delete()
        await message.bot.delete_message(chat_id=data.get("msg_chat_id"), message_id=data.get("msg_id"))
        msg = await message.answer(
            await show_content_folder(data.get("main_message"))
            + f"\n\nВведите название папки/файла, но учтите, если название будет без расширения, то создаться папка",
            reply_markup= await buttons.inline_button_back()
        )
        await state.update_data(msg_id=msg.message_id, msg_chat_id=msg.chat.id)
    except ValueError:
        await message.delete()
        err_msg = await message.answer("Пожалуйста, введите цифру")
        await asyncio.sleep(3)
        await err_msg.delete()
    except KeyError:
        await message.delete()
        err_msg = await message.answer("Вы ввели номер, которого нету в списке. Пожалуйста, введите соответствующий номер")
        await asyncio.sleep(3)
        await err_msg.delete()
    except PermissionError:
        await message.delete()
        err_msg = await message.answer("Похоже, вы выбрали папку/файл, где вам отказали в доступе. Лучше так не делать...")
        await asyncio.sleep(3)
        await err_msg.delete()

@router.message(FileSysStates.change_path)
async def change_path(message: types.Message, state: FSMContext):
    current_path = await current_directory(message)
    data = await state.get_data()
    content = await get_folder_content(current_path)
    try:
        new_path = await change_path_directory(current_path, content, int(message.text))
        await message.delete()
        if new_path == None:
            await History.add_log(
                message.from_user.id,
                message.from_user.username,
                LogsAction.CHANGE,
                False,
                {
                    "path": current_path,
                    "new_folder_file": current_path + message.text,
                    "error": "empty",
                    "state": str(await state.get_state()),
                    "chat_type": message.chat.type,
                }
            )
            err_msg = await message.answer("Данной директории нету в текущей директории")
            await asyncio.sleep(3)
            await err_msg.delete()
            return
        if new_path == "is_file":
            await History.add_log(
                message.from_user.id,
                message.from_user.username,
                LogsAction.CHANGE,
                False,
                {
                    "path": current_path,
                    "new_folder_file": current_path + message.text,
                    "error": new_path,
                    "state": str(await state.get_state()),
                    "chat_type": message.chat.type,
                }
            )
            err_msg = await message.answer("В файл невозможно переместиться")
            await asyncio.sleep(3)
            await err_msg.delete()
            return
        if not new_path[-1] == "/":
            new_path += "/"
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.CHANGE,
            True,
            {
                "path": current_path,
                "new_folder_file": new_path,
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await update_path(message, new_path)
        await message.bot.edit_message_text(
            chat_id=data.get("msg_chat_id"),
            message_id=data.get("msg_id"),
            text=await show_content_folder(
                data.get("main_message")) + f"\n\nВведите цифру папки/файла, в которую вы хотите переместиться",
            reply_markup=await buttons.inline_buttons_change_directory()
        )
    except ValueError:
        msg = message.text
        await message.delete()
        if not msg[-1] == "/":
            msg += "/"
        if await check_absolute_folder(message.text):
            await History.add_log(
                message.from_user.id,
                message.from_user.username,
                LogsAction.CHANGE,
                True,
                {
                    "path": current_path,
                    "new_folder_file": msg,
                    "state": str(await state.get_state()),
                    "chat_type": message.chat.type,
                }
            )
            await update_path(message, message.text)
            await message.bot.edit_message_text(
                chat_id=data.get("msg_chat_id"),
                message_id=data.get("msg_id"),
                text=await show_content_folder(
                    data.get("main_message")) + f"\n\nВведите цифру папки/файла, в которую вы хотите переместиться",
                reply_markup=await buttons.inline_buttons_change_directory()
            )
        else:
            await History.add_log(
                message.from_user.id,
                message.from_user.username,
                LogsAction.CHANGE,
                False,
                {
                    "path": current_path,
                    "new_folder_file": msg,
                    "error": "empty",
                    "state": str(await state.get_state()),
                    "chat_type": message.chat.type,
                }
            )
            err_msg = await message.answer("Был введен неправильный путь или его не существует")
            await asyncio.sleep(3)
            await err_msg.delete()

@router.callback_query(FileSysStates.change_path, F.data == "В родительскую директорию")
async def parent_directory(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    current_path = await current_directory(message)
    new_path = await one_level_up(current_path)
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.PARENT_DIRECTORY,
        True,
        {
            "path": current_path,
            "new_folder_file": new_path,
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await update_path(message, new_path)
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text=await show_content_folder(data.get("main_message")) + f"\n\nВведите цифру папки/файла, в которую вы хотите переместиться",
        reply_markup= await buttons.inline_buttons_change_directory()
    )