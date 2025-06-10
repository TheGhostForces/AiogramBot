from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from app.fsm.choose_states import ChooseState
from app.fsm.sys_states import SysStates
from app.utils import buttons
from app.utils.sys import prevent_sleep, get_system_uptime, get_uploading_components, get_process_list, screenshot, \
    shutdown_or_restart_pc

router = Router()


@router.message(SysStates.sys_actions)
async def choose_action_sys(message: Message, state: FSMContext):
    data = await state.get_data()
    mode = data.get("mode", 1)
    if message.text == "⬅":
        await message.delete()
        if mode == 1:
            await state.clear()
            await state.set_state(ChooseState.choosing)
            await buttons.show_buttons_choice(message, state)
        else:
            await buttons.show_buttons_sys(message, state, mode - 1)
            await state.update_data(mode=mode - 1)
    elif message.text == "➡":
        await message.delete()
        if mode < 4:
            await buttons.show_buttons_sys(message, state, mode + 1)
            await state.update_data(mode=mode + 1)
    elif message.text == "Пробудить ПК":
        await message.delete()
        await prevent_sleep()
    elif message.text == "Время работы системы":
        await message.delete()
        uptime, boot_time = await get_system_uptime()
        await message.answer(f"Время запуска системы: {boot_time}\nВремя работы системы: {str(uptime).split(".")[0]}")
    elif message.text == "Загрузка CPU, RAM, GPU и т.д.":
        await message.delete()
        await get_uploading_components(message)
    elif message.text == "Посмотреть все процессы":
        await message.delete()
        text = await get_process_list()
        await message.answer(text)
    elif message.text == "Сделать скриншот":
        await message.delete()
        file = FSInputFile(await screenshot())
        await message.answer_photo(file, caption=f"Скришнот рабочего стола")
    elif message.text == "Выключить ПК":
        await message.delete()
        await state.update_data(mode_del_res="shutdown")
        await state.set_state(SysStates.shutdown_restart)
        await buttons.show_buttons_shutdown_or_restart(message)
    elif message.text == "Перезагрузка ПК":
        await message.delete()
        await state.update_data(mode_del_res="restart")
        await state.set_state(SysStates.shutdown_restart)
        await buttons.show_buttons_shutdown_or_restart(message)

@router.message(SysStates.shutdown_restart)
async def shutdown_restart(message: Message, state: FSMContext):
    data = await state.get_data()
    mode = data.get("mode_del_res")
    if message.text == "Да":
        await state.clear()
        await shutdown_or_restart_pc(mode)
        if mode == "shutdown":
            await message.answer("Выключаю...")
        elif mode == "restart":
            await message.answer("Перезагружаю...")
    if message.text == "Нет":
        await state.set_state(SysStates.sys_actions)
        await buttons.show_buttons_sys(message, state,4)