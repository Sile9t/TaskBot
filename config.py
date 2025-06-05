import os
from typing import List
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from configobj import ConfigObj
from pydantic_settings import BaseSettings, SettingsConfigDict

config = ConfigObj("config.ini")

class Settings(BaseSettings):
    TG_KEY: str = config['telegram']['key']

    BOT_TOKEN: str
    ADMIN_IDS: List[int]

    REDIS: str

    DB_USER: str = config['database']['user']
    DB_PASSWORD: str = config['database']['password']
    DB_HOST: str = config['database']['host']
    DB_PORT: str = config['database']['port']
    DB_NAME: str = config['database']['postgres']['name']

    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self):
        return (f"sqlite+aiosqlite:///instance/{config['database']['sqlite']['name']}") # connection for local async sqlite database
    
settings = Settings()

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# storage = RedisStorage.from_url(settings.REDIS)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
admins = settings.ADMIN_IDS

#TODO: change to log folder where will be log files for every day
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dump.log")
logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)
database_url = settings.get_db_url()