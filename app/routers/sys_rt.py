import asyncio

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from app.database.enums import LogsAction
from app.database.repository import History
from app.fsm.sys_states import SysStates
from app.utils import buttons
from app.utils.sys import prevent_sleep, get_system_uptime, get_uploading_components, screenshot, \
    shutdown_or_restart_pc, get_process_list, kill_process_by_pid

router = Router()


@router.callback_query(SysStates.sys_actions, F.data == "Пробудить")
async def wake_up(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    await prevent_sleep()
    await callback.answer("Компьютер проснулся")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.WAKE_UP,
        True,
        {
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )

@router.callback_query(SysStates.sys_actions, F.data == "Время")
async def working_time(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    uptime, boot_time = await get_system_uptime()
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.WORKING_TIME,
        True,
        {
            "launch_time": boot_time,
            "working_time": str(uptime).split(".")[0],
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text=f"Время запуска системы: {boot_time}\nВремя работы системы: {str(uptime).split(".")[0]}\n\n"
             f"Выберите действие: ",
        reply_markup= await buttons.inline_buttons_sys()
    )

@router.callback_query(SysStates.sys_actions, F.data == "Загрузка")
async def loading_components(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.LOADING_COMPONENTS,
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
        text=f"{await get_uploading_components()}\n\n"
             f"Выберите действие: ",
        reply_markup= await buttons.inline_buttons_sys()
    )

@router.callback_query(SysStates.sys_actions, F.data == "Скриншот")
async def take_screenshot(callback: types.CallbackQuery, state: FSMContext):
    path = await screenshot()
    file = FSInputFile(path)
    data = await state.get_data()
    message = data.get("main_message")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.TAKE_SCREENSHOT,
        True,
        {
            "screenshot": str(path),
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await callback.message.answer_photo(file, caption=f"Скришнот рабочего стола")
    await callback.message.bot.delete_message(chat_id=data.get("msg_chat_id"), message_id=data.get("msg_id"))
    msg = await callback.message.answer(
        f"Выберите действие: ",
        reply_markup=await buttons.inline_buttons_sys()
    )
    await state.update_data(msg_id=msg.message_id, msg_chat_id=msg.chat.id)

@router.callback_query(SysStates.sys_actions, F.data == "Все процессы")
async def all_processes(callback: types.CallbackQuery, state: FSMContext):
    filename, file = await get_process_list()
    data = await state.get_data()
    message = data.get("main_message")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.ALL_PROCESSES,
        True,
        {
            "file_with_all_processes": str(filename),
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await callback.message.answer_document(file, caption=f"Список всех процессов: ")
    await callback.message.bot.delete_message(chat_id=data.get("msg_chat_id"), message_id=data.get("msg_id"))
    msg = await callback.message.answer(
        f"Выберите действие: ",
        reply_markup=await buttons.inline_buttons_sys()
    )
    await state.update_data(msg_id=msg.message_id, msg_chat_id=msg.chat.id)

@router.callback_query(SysStates.kill_process, F.data == "Назад в системные действия")
async def back_to_sys_actions(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.BACK_TO_SYS_ACTIONS,
        True,
        {
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await state.set_state(SysStates.sys_actions)
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text="Выберите действие: ",
        reply_markup= await buttons.inline_buttons_sys()
    )

@router.callback_query(SysStates.sys_actions, F.data == "Закрыть")
async def kill_process(callback: types.CallbackQuery, state: FSMContext):
    filename, file = await get_process_list()
    data = await state.get_data()
    message = data.get("main_message")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.KILL_PROCESSES,
        True,
        {
            "file_with_all_processes": str(filename),
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await callback.message.answer_document(file, caption=f"Список всех процессов: ")
    await callback.message.bot.delete_message(chat_id=data.get("msg_chat_id"), message_id=data.get("msg_id"))
    msg = await callback.message.answer(
        f"Введите PID процесса, который хотите закрыть",
        reply_markup=await buttons.inline_button_back_to_sys()
    )
    await state.update_data(msg_id=msg.message_id, msg_chat_id=msg.chat.id)
    await state.set_state(SysStates.kill_process)

@router.message(SysStates.kill_process)
async def entry_pid(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        name_process, text = await kill_process_by_pid(int(message.text))
        if name_process == "Not_found":
            await History.add_log(
                message.from_user.id,
                message.from_user.username,
                LogsAction.ENTRY_PID,
                False,
                {
                    "error": name_process,
                    "message": message.text,
                    "state": str(await state.get_state()),
                    "chat_type": message.chat.type,
                }
            )
        else:
            await History.add_log(
                message.from_user.id,
                message.from_user.username,
                LogsAction.ENTRY_PID,
                True,
                {
                    "name_process": name_process,
                    "message": message.text,
                    "state": str(await state.get_state()),
                    "chat_type": message.chat.type,
                }
            )
        await message.delete()
        await message.bot.edit_message_text(
            chat_id=data.get("msg_chat_id"),
            message_id=data.get("msg_id"),
            text=text + f"\n\nВведите PID процесса, который хотите закрыть",
            reply_markup= await buttons.inline_button_back_to_sys()
        )
    except ValueError:
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.ENTRY_PID,
            False,
            {
                "error": "ValueError",
                "message": message.text,
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await message.delete()
        err_msg = await message.answer("Пожалуйста, введите цифру")
        await asyncio.sleep(3)
        await err_msg.delete()

@router.callback_query(SysStates.sys_actions, F.data.in_({"Выключить", "Перезагрузка"}))
async def shutdown_restart(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    action = callback.data
    if action == "Выключить":
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.SHUTDOWN,
            True,
            {
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await state.update_data(mode_del_res="shutdown")
    elif action == "Перезагрузка":
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.RESTART,
            True,
            {
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await state.update_data(mode_del_res="restart")
    await state.set_state(SysStates.shutdown_restart)
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text="Вы уверены?",
        reply_markup= await buttons.inline_buttons_yes_no()
    )

@router.callback_query(SysStates.shutdown_restart, F.data.in_({"Да", "Нет"}))
async def answer_for_shutdown_restart(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    action = callback.data
    mode =  data.get("mode_del_res")
    if action == "Да":
        await shutdown_or_restart_pc(mode)
        if mode == "shutdown":
            await History.add_log(
                message.from_user.id,
                message.from_user.username,
                LogsAction.ANSWER_SHUTDOWN,
                True,
                {
                    "action": action,
                    "mode": mode,
                    "state": str(await state.get_state()),
                    "chat_type": message.chat.type,
                }
            )
            await callback.answer("Выключаю...")
        elif mode == "restart":
            await History.add_log(
                message.from_user.id,
                message.from_user.username,
                LogsAction.SHUTDOWN,
                True,
                {
                    "action": action,
                    "mode": mode,
                    "state": str(await state.get_state()),
                    "chat_type": message.chat.type,
                }
            )
            await callback.answer("Перезагружаю...")
    if action == "Нет":
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.USER_DECLINED,
            True,
            {
                "action": action,
                "mode": mode,
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await state.set_state(SysStates.sys_actions)
        await callback.message.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=data.get("msg_id"),
            text="Выберите действие: ",
            reply_markup=await buttons.inline_buttons_sys()
        )
