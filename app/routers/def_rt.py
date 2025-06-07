import asyncio
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

@router.message()
async def default_handler(message: Message,state: FSMContext):
    await state.clear()
    msg = await message.answer("Пожалуйста, отправьте команду /start для начала.", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(3)
    await message.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)