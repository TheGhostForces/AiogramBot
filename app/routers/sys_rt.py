from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from app.fsm.choose_states import ChooseState
from app.fsm.sys_states import SysStates
from app.utils import buttons
from app.utils.sys import prevent_sleep, get_system_uptime, get_uploading_components, screenshot, \
    shutdown_or_restart_pc


router = Router()


@router.callback_query(SysStates.sys_actions, F.data == "Назад в главное меню")
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(ChooseState.choosing)
    await callback.message.bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=data.get("msg_id"),
        text="Выберите действие: ",
        reply_markup= await buttons.inline_buttons_choose()
    )

@router.callback_query(SysStates.sys_actions, F.data == "Пробудить")
async def wake_up(callback: types.CallbackQuery):
    await prevent_sleep()
    await callback.answer("Компьютер проснулся")

@router.callback_query(SysStates.sys_actions, F.data == "Время")
async def working_time(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    uptime, boot_time = await get_system_uptime()
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
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text=f"{await get_uploading_components()}\n\n"
             f"Выберите действие: ",
        reply_markup= await buttons.inline_buttons_sys()
    )

@router.callback_query(SysStates.sys_actions, F.data == "Все процессы")
async def all_processes(callback: types.CallbackQuery, state: FSMContext):
    # text = await get_process_list()
    pass # Переработать функционал

@router.callback_query(SysStates.sys_actions, F.data == "Скриншот")
async def take_screenshot(callback: types.CallbackQuery, state: FSMContext):
    file = FSInputFile(await screenshot())
    data = await state.get_data()
    await callback.message.answer_photo(file, caption=f"Скришнот рабочего стола")
    await callback.message.bot.delete_message(chat_id=data.get("msg_chat_id"), message_id=data.get("msg_id"))
    msg = await callback.message.answer(
        f"Выберите действие: ",
        reply_markup=await buttons.inline_buttons_sys()
    )
    await state.update_data(msg_id=msg.message_id, msg_chat_id=msg.chat.id)

@router.callback_query(SysStates.sys_actions, F.data.in_({"Выключить", "Перезагрузка"}))
async def shutdown_restart(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    action = callback.data
    if action == "Выключить":
        await state.update_data(mode_del_res="shutdown")
    elif action == "Перезагрузка":
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
    action = callback.data
    mode =  data.get("mode_del_res")
    if action == "Да":
        await shutdown_or_restart_pc(mode)
        if mode == "shutdown":
            await callback.answer("Выключаю...")
        elif mode == "restart":
            await callback.answer("Перезагружаю...")
    if action == "Нет":
        await state.set_state(SysStates.sys_actions)
        await callback.message.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=data.get("msg_id"),
            text="Выберите действие: ",
            reply_markup=await buttons.inline_buttons_sys()
        )
