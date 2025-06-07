import asyncio

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from app.utils import buttons
from app.fsm.functions_for_trusted import Functions
from app.utils.file_sys import show_content_folder

router = Router()

@router.message(Functions.choosing)
async def choose_2_btn(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == "Управление файловой системой ПК":
        await message.answer("Было выбрано: Управление файловой системой ПК", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Functions.file_system)
        await buttons.show_buttons_file_system(message)
        await message.bot.delete_messages(chat_id=message.chat.id, message_ids=[message.message_id, data.get("msg")])
        await show_content_folder(message)
    if message.text == "Системные действия с ПК":
        await message.delete()
        await message.answer("Было выбрано: Системные действия с ПК", reply_markup=types.ReplyKeyboardRemove())
        await message.bot.delete_messages(chat_id=message.chat.id, message_ids=[message.message_id, data.get("msg")])
    if message.text == "Логи":
        await message.delete()
        await message.answer("Было выбрано действие: Логи", reply_markup=types.ReplyKeyboardRemove())
        await message.bot.delete_messages(chat_id=message.chat.id, message_ids=[message.message_id, data.get("msg")])