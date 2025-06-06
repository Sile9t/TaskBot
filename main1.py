import asyncio
import locale
from loguru import logger
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram_dialog import setup_dialogs
from config import bot, dp
from taskbot.dao.database_middleware import DatabaseMiddlewareWithCommit, DatabaseMiddlewareWithoutCommit
from taskbot.dao.seed import seed

from taskbot.admin.router import admin_router

from taskbot.region.dialog import region_create_dialog, regions_read_dialog, region_update_dialog, region_delete_dialog
from taskbot.region.router import region_router

# from taskbot.user.user import user_router
from taskbot.user.router import user_router
from taskbot.user.dialog import user_create_dialog, users_read_dialog, user_update_dialog, user_delete_dialog 

from taskbot.role.router import role_router
from taskbot.role.dialog import role_create_dialog, roles_read_dialog, role_update_dialog, role_delete_dialog

from taskbot.status.router import status_router
from taskbot.status.dialog import status_create_dialog, statuses_read_dialog, status_update_dialog, status_delete_dialog

from taskbot.priority.router import priority_router
from taskbot.priority.dialog import priority_create_dialog, priorities_read_dialog, priority_update_dialog, priority_delete_dialog

from taskbot.task.router import task_router
from taskbot.task.dialog import task_create_dialog, tasks_read_dialog, task_update_dialog, task_delete_dialog, task_status_change_dialog, task_priority_change_dialog, task_region_change_dialog


async def set_commands():
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

async def start_bot():
    await set_commands()
    logger.success("Бот успешно запущен.")

async def stop_bot():
    logger.error("Бот остановлен!")

#TODO: fix tasks cancellation on bot stoping
async def main():
    set_russian_locale()
    await seed()

    setup_dialogs(dp)
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())

    dp.include_router(admin_router)

    dp.include_routers(region_create_dialog, regions_read_dialog, region_update_dialog, region_delete_dialog, region_router)

    dp.include_routers(role_create_dialog, roles_read_dialog, role_update_dialog, role_delete_dialog, role_router)
    
    dp.include_routers(user_create_dialog, users_read_dialog, user_update_dialog, user_delete_dialog, user_router)

    dp.include_routers(status_router, status_create_dialog, statuses_read_dialog, status_update_dialog, status_delete_dialog)

    dp.include_routers(priority_router, priority_create_dialog, priorities_read_dialog, priority_update_dialog, priority_delete_dialog)

    dp.include_routers(task_router, task_create_dialog, tasks_read_dialog, task_update_dialog, task_delete_dialog, task_status_change_dialog, task_priority_change_dialog, task_region_change_dialog)
        
    # dp.include_router(user_router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except asyncio.exceptions.CancelledError:
        pass
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
