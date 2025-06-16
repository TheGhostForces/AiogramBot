import asyncio
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from app.database.enums import LogsAction
from app.database.repository import VerifyUser, History
from app.fsm.log_states import LogStates
from app.utils import buttons
from app.fsm.choose_states import ChooseState
from app.fsm.file_sys_states import FileSysStates
from app.fsm.sys_states import SysStates
from app.utils.file_sys import show_content_folder, check_exists_folder, current_directory


router = Router()


@router.callback_query(ChooseState.choosing, F.data == "Файловая система")
async def choose_file_sys(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Было выбрано: Управление файловой системой ПК")
    data = await state.get_data()
    message = data.get("main_message")
    current_path = await current_directory(message)
    await state.set_state(FileSysStates.file_system)
    if not await check_exists_folder(current_path):
        await VerifyUser.update_path(message.from_user.id, message.from_user.username, "C:/")
        await callback.message.bot.edit_message_text(
            chat_id=data.get("msg_chat_id"),
            message_id=data.get("msg_id"),
            text=await show_content_folder(
                data.get("main_message")),
            reply_markup=await buttons.inline_buttons_file_sys()
        )
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.FILE_SYSTEM,
            True,
            {
                "f_data": str(callback.data),
                "path": current_path,
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        err_msg = await message.answer("Ранее выбраный путь не существует \nВы были возвращены на C:/")
        await asyncio.sleep(2)
        await err_msg.delete()
    else:
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.FILE_SYSTEM,
            True,
            {
                "f_data": str(callback.data),
                "path": current_path,
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await callback.message.bot.edit_message_text(
            chat_id=data.get("msg_chat_id"),
            message_id=data.get("msg_id"),
            text=await show_content_folder(data.get("main_message")),
            reply_markup= await buttons.inline_buttons_file_sys()
        )

@router.callback_query(ChooseState.choosing, F.data == "Системные действия")
async def choose_sys(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Было выбрано: Системные действия")
    data = await state.get_data()
    message = data.get("main_message")
    await state.set_state(SysStates.sys_actions)
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.SYSTEM_ACTION,
        True,
        {
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text="Выберите действие: ",
        reply_markup=await buttons.inline_buttons_sys()
    )

@router.callback_query(ChooseState.choosing, F.data == "Логи")
async def choose_logs(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Логи")
    data = await state.get_data()
    message = data.get("main_message")
    await state.set_state(LogStates.choice_log)
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.LOGS,
        True,
        {
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text="Выберите действие: ",
        reply_markup=await buttons.inline_button_choice_logs()
    )