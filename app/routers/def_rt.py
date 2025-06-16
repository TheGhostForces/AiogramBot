import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from app.database.repository import History
from app.database.enums import LogsAction
from app.fsm.choose_states import ChooseState
from app.utils import buttons

router = Router()


@router.message()
async def default_handler(message: Message,state: FSMContext):
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.DEFAULT,
        True,
        {
            "message": message.text,
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await message.delete()
    msg = await message.answer("Пожалуйста, отправьте команду /start для начала.", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(3)
    await message.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)

@router.callback_query(F.data == "Назад в главное меню")
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.BACK_TO_MAIN_MENU,
        True,
        {
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await state.set_state(ChooseState.choosing)
    await callback.message.bot.edit_message_text(
        chat_id=data.get("msg_chat_id"),
        message_id=data.get("msg_id"),
        text="Выберите действие: ",
        reply_markup= await buttons.inline_buttons_choose()
    )