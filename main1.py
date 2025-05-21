import asyncio
import locale
from loguru import logger
from taskbot import create_app
from telegram import Update
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram_dialog import setup_dialogs
from config import bot, dp
from taskbot.dao.database_middleware import DatabaseMiddlewareWithCommit, DatabaseMiddlewareWithoutCommit
from taskbot.admin.admin import admin_router
from taskbot.admin.role import role_router
from taskbot.admin.task import task_router
from taskbot.admin.employee import employee_router
from taskbot.user.user import user_router
from taskbot.role.dialog import role_create_dialog, roles_read_dialog, role_update_dialog, role_delete_dialog
from taskbot.task.dialog import task_dialog
from taskbot.dao.seed import seed

async def set_commands():
    commands = [
        BotCommand(command='help', description='Список команд'),
        BotCommand(command='start', description='Старт'),
        BotCommand(command='admin_panel', description='Меню администрирования'),
        BotCommand(command='role_menu', description='Меню для должностей'),
        BotCommand(command='task_menu', description='Меню для задач'),
        # BotCommand(command='task_list', description='Список задач'),
        # BotCommand(command='task_add', description='Добавить задачу'),
        # BotCommand(command='task_edit', description='Редактировать задачу'),
        # BotCommand(command='task_close', description='Закрыть задачу'),
        # BotCommand(command='task_delete', description='Удалить задачу'),
        BotCommand(command='employee_menu', description='Меню для сотрудников'),
        # BotCommand(command='employee_list', description='Список сотрудников'),
        # BotCommand(command='employee_add', description='Добавить сотрудника'),
        # BotCommand(command='employee_edit', description='Редактировать информацию о сотруднике'),
        # BotCommand(command='employee_delete', description='Удалить информацию о сотруднике'),
        # BotCommand(command='employee_change_role', description='Изменить роль сотрудника'),
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
    dp.include_router(role_create_dialog)
    dp.include_router(roles_read_dialog)
    dp.include_router(role_update_dialog)
    dp.include_router(role_delete_dialog)
    dp.include_router(role_router)
    dp.include_router(task_router)
    dp.include_router(task_dialog)
    dp.include_router(employee_router)
    dp.include_router(user_router)

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
