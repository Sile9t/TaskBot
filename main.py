import asyncio
import locale
from loguru import logger
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram_dialog import setup_dialogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.triggers.cron import CronTrigger
from config import settings, dp
from taskbot.dao.database_middleware import DatabaseMiddlewareWithCommit, DatabaseMiddlewareWithoutCommit
from taskbot.jobs.jobs import send_daily_digest
from taskbot.dao.seed import seed

from taskbot.auth.auth import AuthenticateMiddleware

from taskbot.general.router import general_router

from taskbot.admin.router import admin_router

from taskbot.region.dialog import region_create_dialog, regions_read_dialog, region_update_dialog, region_delete_dialog, region_wire_chat_dialog
from taskbot.region.router import region_router

from taskbot.user.router import user_router
from taskbot.user.dialog import user_create_dialog, users_read_dialog, user_update_dialog, user_delete_dialog 

from taskbot.role.router import role_router
from taskbot.role.dialog import role_create_dialog, roles_read_dialog, role_update_dialog, role_delete_dialog

from taskbot.status.router import status_router
from taskbot.status.dialog import status_create_dialog, statuses_read_dialog, status_update_dialog, status_delete_dialog

from taskbot.priority.router import priority_router
from taskbot.priority.dialog import priority_create_dialog, priorities_read_dialog, priority_update_dialog, priority_delete_dialog

from taskbot.task.router import task_router
from taskbot.task.dialog import task_create_dialog, tasks_read_dialog, task_update_dialog, task_delete_dialog, task_status_change_dialog, task_priority_change_dialog, task_region_change_dialog, task_set_performers_dialog, task_change_dates_dialog


async def set_commands(bot: Bot):
    commands = [
        # BotCommand(command='help', description='Список команд'),
        BotCommand(command='start', description='Старт'),
        BotCommand(command='admin_panel', description='Панель администрирования'),
        BotCommand(command='role_menu', description='Меню для должностей'),
        BotCommand(command='task_menu', description='Меню для задач'),
        BotCommand(command='user_menu', description='Меню для пользователей'),
        # BotCommand(command='employee_menu', description='Меню для сотрудников'),
        BotCommand(command='region_menu', description='Меню для регионов'),
        BotCommand(command='status_menu', description='Меню для статусов задач'),
        BotCommand(command='priority_menu', description='Меню для приоритетов задач'),
        BotCommand(command='priority_menu', description='Меню для приоритетов задач'),
        BotCommand(command='cancel', description='Отмена сценария'),
    ]
    
    await bot.set_my_commands(commands, BotCommandScopeDefault())

def set_russian_locale():
    try:
        # Пробуем установить локаль для Windows
        locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')
    except locale.Error:
        try:
            # Пробуем установить локаль для Linux/macOS
            locale.setlocale(locale.LC_TIME, 'ru_RU.utf8')
        except locale.Error:
            # Игнорируем ошибку, если локаль не поддерживается
            pass

async def start_bot(bot: Bot):
    await set_commands(bot)
    logger.success("Бот успешно запущен.")

async def stop_bot():
    logger.error("Бот остановлен!")

#TODO: fix tasks cancellation on bot stoping
async def main():
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    jobstores = {
        'default': SQLAlchemyJobStore(settings.get_jobs_url())
    }
    executors = {
        'default': AsyncIOExecutor()
    }
    
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow", jobstores=jobstores, executors=executors)
    
    scheduler.add_job(
        send_daily_digest,
        # trigger=CronTrigger(second=10),
        trigger=CronTrigger(hour=8, minute=0),
        id="daily_task_digest",
        name='Ежедневная рассылка задач',
        replace_existing=True,
    )
    
    set_russian_locale()
    await seed()

    setup_dialogs(dp)
    dp.update.middleware(ChatActionMiddleware())
    dp.update.middleware.register(AuthenticateMiddleware())
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())

    dp.include_router(admin_router)

    dp.include_routers(region_create_dialog, regions_read_dialog, region_update_dialog, region_delete_dialog, region_router, region_wire_chat_dialog)

    dp.include_routers(role_create_dialog, roles_read_dialog, role_update_dialog, role_delete_dialog, role_router)
    
    dp.include_routers(user_create_dialog, users_read_dialog, user_update_dialog, user_delete_dialog, user_router)

    dp.include_routers(status_router, status_create_dialog, statuses_read_dialog, status_update_dialog, status_delete_dialog)

    dp.include_routers(priority_router, priority_create_dialog, priorities_read_dialog, priority_update_dialog, priority_delete_dialog)

    dp.include_routers(task_router, task_create_dialog, tasks_read_dialog, task_update_dialog, task_delete_dialog, task_status_change_dialog, task_priority_change_dialog, task_region_change_dialog, task_set_performers_dialog, task_change_dates_dialog)

    dp.include_router(notification_router)

    dp.include_router(general_router)
        
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        scheduler.start()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except asyncio.exceptions.CancelledError:
        pass
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
