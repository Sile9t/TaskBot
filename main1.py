import asyncio
from loguru import logger
from taskbot import create_app
from telegram import Update
from aiogram.types import BotCommand, BotCommandScopeDefault
from config import bot, dp
from taskbot.dao.database_middleware import DatabaseMiddlewareWithCommit, DatabaseMiddlewareWithoutCommit
from taskbot.admin.admin import admin_router
from taskbot.admin.role import role_router
from taskbot.user.user import user_router
from taskbot.dao.seed import seed

"""
Точка входа в программу.
По всей видимости, при желании создать автоматическую рассылку сообщений, придется
все переделывать в asyncio, чтобы убрать бота в один поток, а средство для
рассылки - в другой.
"""
# application = create_app()

async def set_commands():
    commands = [
        BotCommand(command='help', description='Список команд'),
        BotCommand(command='start', description='Старт'),
        BotCommand(command='admin_panel', description='Меню администрирования'),
        BotCommand(command='role_menu', description='Меню для должностей'),
        BotCommand(command='task_menu', description='Меню для задач'),
        BotCommand(command='task_list', description='Список задач'),
        BotCommand(command='task_add', description='Добавить задачу'),
        BotCommand(command='task_edit', description='Редактировать задачу'),
        BotCommand(command='task_close', description='Закрыть задачу'),
        BotCommand(command='task_delete', description='Удалить задачу'),
        BotCommand(command='employee_menu', description='Меню для сотрудников'),
        BotCommand(command='employee_list', description='Список сотрудников'),
        BotCommand(command='employee_add', description='Добавить сотрудника'),
        BotCommand(command='employee_edit', description='Редактировать информацию о сотруднике'),
        BotCommand(command='employee_delete', description='Удалить информацию о сотруднике'),
        BotCommand(command='employee_change_role', description='Изменить роль сотрудника'),
        BotCommand(command='help', description='Список команд'),
    ]
    
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def start_bot():
    await set_commands()
    logger.info("Бот успешно запущен.")

async def stop_bot():
    await bot.session.close()
    logger.info("Бот остановлен!")


async def main():
    await seed()

    dp.update.middleware.register(DatabaseMiddlewareWithCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())

    dp.include_router(admin_router)
    dp.include_router(role_router)
    dp.include_router(user_router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    
    try:
        await bot.delete_webhook(drop_pending_updates=True, request_timeout=1)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(application.run_polling(allowed_updates=Update.ALL_TYPES))