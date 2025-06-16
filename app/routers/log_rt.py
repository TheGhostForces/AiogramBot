from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from app.database.enums import LogsAction
from app.database.repository import History
from app.fsm.log_states import LogStates
from app.utils import buttons
from app.utils.log import get_logs_bot_list


router = Router()


@router.callback_query(LogStates.choice_log, F.data == "Логи бота")
async def bot_logs(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("main_message")
    time, filename = await get_logs_bot_list()
    file = FSInputFile(filename)
    await History.add_log(
        message.from_user.id,
        message.from_user.username,
        LogsAction.BOT_LOGS,
        True,
        {
            "log_path": str(filename),
            "f_data": str(callback.data),
            "state": str(await state.get_state()),
            "chat_type": message.chat.type,
        }
    )
    await callback.message.answer_document(file, caption=f"Логи бота за {time.strftime('%Y-%m-%d %H:%M:%S')}")
    await callback.message.bot.delete_message(chat_id=data.get("msg_chat_id"), message_id=data.get("msg_id"))
    msg = await callback.message.answer(
        f"Выберите действие: ",
        reply_markup=await buttons.inline_button_choice_logs()
    )
    await state.update_data(msg_id=msg.message_id, msg_chat_id=msg.chat.id)