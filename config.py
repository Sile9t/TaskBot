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
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

config = ConfigObj("config.ini")

class Settings(BaseSettings):
    BOT_TOKEN: str = config['telegram']['token']

    JOBS: str = config['database']['jobs']['name']

    DB_USER: str = config['database']['user']
    DB_PASSWORD: str = config['database']['password']
    DB_HOST: str = config['database']['host']
    DB_PORT: str = config['database']['port']
    DB_NAME: str = config['database']['sqlite']['name']

    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self):
        return (f"sqlite+aiosqlite:///instance/{self.DB_NAME}") # connection for local async sqlite database
    
    def get_jobs_url(self):
        return (f"sqlite:///jobs/{self.JOBS}") # connection for local jobs sqlite database
    
settings = Settings()

# storage = RedisStorage.from_url(settings.REDIS)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

#TODO: change to log folder where will be log files for every day
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs/dump.log")
logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)
database_url = settings.get_db_url()