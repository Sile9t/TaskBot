import asyncio
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from taskbot.scheduler.scheduler import TaskNotifier

notification_router = Router()

@notification_router.message(Command("notification_add"))
# @notification_router.message(F.text.casefold() == "notification_add")
async def notification_add(message: Message, session_without_commit: AsyncSession, notifier: TaskNotifier) -> None:
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов кнопки notification/notification_add")

    await notifier.addNotificationsForThreeLastDays(session=session_without_commit,task_id=1)
    await message.answer(
        "Task notifier planning notification",
        reply_markup=ReplyKeyboardRemove(),
    )
