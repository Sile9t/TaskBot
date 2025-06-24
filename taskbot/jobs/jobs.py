from datetime import date, datetime, timedelta
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from loguru import logger

from taskbot.dao.database import async_session_maker
from taskbot.dao.models import Task
from taskbot.dao.dao import TaskDAO
from config import settings

def getTaskDeadlineDate(task: Task):
    return task.deadline.date

class DailyTaskDigestSender:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(self):
        today = date.today()
        logger.info(f"Запуск утренней рассылки задач исполнителям на {today}")

        async with async_session_maker() as session:
            tasks = await TaskDAO.find_all(
                session,
                filters=None
            )
            
            tasks = sorted(tasks, key=lambda task: task.deadline)
            tasks = [t for t in tasks if t.is_active & (t.status_id != 1)]

            user_task_map: dict[int, list[str]] = {}

            for task in tasks:
                text_block = task.toBeautifiedText()

                for performer in task.performers:
                    user_task_map.setdefault(performer.telegram_id, []).append(text_block)

            for telegram_id, messages in user_task_map.items():
                try:
                    full_text = (
                        "🌅 <b>Доброе утро!</b>\n"
                        "Вот задачи, требующие вашего внимания:\n\n" +
                        "\n\n".join(messages)
                    )
                    await self.bot.send_message(chat_id=telegram_id, text=full_text)
                    logger.info(f"Уведомление отправлено пользователю {telegram_id}")
                except Exception as e:
                    logger.error(f"Ошибка при отправке сообщения пользователю {telegram_id}: {e}")

async def send_daily_digest():
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        digest = DailyTaskDigestSender(bot)
        await digest()
    finally:
        await bot.session.close()
