import os
from loguru import logger
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_NAME: str
    BOT_SHORT_DESCRIPTION: str
    BOT_DESCRIPTION: str
    BOT_TOKEN: str

    JOBS_NAME: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self):
        return (f"sqlite+aiosqlite:///instance/{self.DB_NAME}") # connection for local async sqlite database
    
    def get_jobs_url(self):
        return (f"sqlite:///jobs/{self.JOBS_NAME}") # connection for local jobs sqlite database
    
settings = Settings()

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs/dump.log")
logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)
database_url = settings.get_db_url()