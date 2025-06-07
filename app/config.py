from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("Не указан BOT_TOKEN в .env файле")


Config.validate()