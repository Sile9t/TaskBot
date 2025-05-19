import locale
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram_dialog import setup_dialogs
from config import settings
from taskbot.dao.database_middleware import DatabaseMiddlewareWithCommit, DatabaseMiddlewareWithoutCommit
from taskbot.admin.admin import admin_router
from taskbot.admin.role import role_router
from taskbot.admin.employee import employee_router
from taskbot.user.user import user_router
from taskbot.dao.seed import seed

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = RedisStorage.from_url(settings.REDIS)
dp = Dispatcher(storage=storage)

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
    set_russian_locale()
    await seed()

    setup_dialogs(dp)
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())
    
    await set_commands()

    dp.include_router(admin_router)
    dp.include_router(role_router)
    dp.include_router(employee_router)
    dp.include_router(user_router)

    logger.success("Бот успешно запущен.")

async def stop_bot():
    logger.error("Бот остановлен!")

dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)
    