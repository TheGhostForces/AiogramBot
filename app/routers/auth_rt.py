import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app.database.enums import LogsAction
from app.fsm.choose_states import ChooseState
from app.database.repository import Users, VerifyUser, History
from app.fsm.auth import AuthStates
from app.utils.buttons import inline_buttons_choose


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.START,
        True,
        {
            "message": message.text,
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await state.clear()
    await message.delete()
    await state.update_data(main_message=message)
    exist_user = await Users.check_user(message.from_user.id, message.from_user.username)
    if not exist_user:
        new_user = await Users.add_user(message.from_user.id, message.from_user.username, 3)
        attempts = new_user.attempts
    else:
        attempts = exist_user.attempts
    if attempts == 0:
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.BLOCKED,
            True,
            {
                "message": message.text,
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await message.answer("Доступ закрыт!", reply_markup=ReplyKeyboardRemove())
        await state.set_state(AuthStates.block)
    if attempts > 0:
        msg_pass = await message.answer("Введите пароль для получения доступа:", reply_markup=ReplyKeyboardRemove())
        await state.update_data(msg_pass=msg_pass.message_id)
        await state.set_state(AuthStates.waiting_for_password)

@router.message(AuthStates.waiting_for_password)
async def processed_password(message: types.Message, state: FSMContext):
    attempts = await Users.check_user_attempts(message.from_user.id, message.from_user.username)
    verify = await VerifyUser.verification_user(message.from_user.id, message.from_user.username, message.text)
    data = await state.get_data()
    if verify:
        await History.add_log(
            message.from_user.id,
            message.from_user.username,
            LogsAction.AUTH_SUCCESS,
            True,
            {
                "message": message.text,
                "state": str(await state.get_state()),
                "chat_type": message.chat.type,
            }
        )
        await message.delete()
        msg_suc = await message.answer("Пароль верный. Доступ открыт!")
        await Users.update_attempts(message.from_user.id, message.from_user.username, 3)
        await state.set_state(ChooseState.choosing)
        await inline_buttons_choose()
        msg = await message.answer("Выберите действие: ", reply_markup=await inline_buttons_choose())
        await state.update_data(msg_id=msg.message_id, msg_chat_id=msg.chat.id)
        await asyncio.sleep(2)
        await message.bot.delete_messages(chat_id=msg_suc.chat.id, message_ids=[msg_suc.message_id, data.get("msg_pass")])
        return
    if attempts > 0:
        attempts -= 1
        await Users.update_attempts(message.from_user.id, message.from_user.username, attempts)
        if attempts > 0:
            await History.add_log(
                message.from_user.id,
                message.from_user.username,
                LogsAction.AUTH_FAIL,
                False,
                {
                    "message": message.text,
                    "state": str(await state.get_state()),
                    "chat_type": message.chat.type,
                }
            )
            await message.delete()
            await message.answer(f"Пароль неверный. У вас осталось {attempts} попыток")
        else:
            await History.add_log(
                message.from_user.id,
                message.from_user.username,
                LogsAction.BLOCKED,
                True,
                {
                    "message": message.text,
                    "state": str(await state.get_state()),
                    "chat_type": message.chat.type,
                }
            )
            await message.delete()
            await message.answer("Доступ закрыт!")
            await state.set_state(AuthStates.block)

@router.message(AuthStates.block)
async def block(message: types.Message, state: FSMContext):
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.BLOCKED,
        True,
        {
            "message": message.text,
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await message.delete()
    await message.answer("Доступ закрыт!")