from aiogram import Bot, Dispatcher
from app.config import Config


bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()