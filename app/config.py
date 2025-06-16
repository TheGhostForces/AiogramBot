from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    @classmethod
    def validate_bot(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("Не указан BOT_TOKEN в .env файле")

    PHOTO_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
    VIDEO_EXT = {".mp4", ".mov", ".avi", ".mkv"}
    AUDIO_EXT = {".mp3", ".wav", ".ogg", ".flac"}
    DOCUMENT_EXT = {".pdf", ".doc", ".docx", ".txt", ".zip", ".rar", ".xlsx", ".csv"}


Config.validate_bot()