import asyncio
from loguru import logger
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from config import settings, bot
from taskbot.dao.dao import TaskDAO
from taskbot.dao.schemas import TaskDto

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info("Вызов команды /start")
    await message.answer(
        f"👋🏻 Привет, {message.from_user.full_name}!\nВыберите дальнейшие действия:",
        reply_markup=None
    )