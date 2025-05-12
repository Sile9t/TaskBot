import asyncio
from loguru import logger
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from config import bot
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.admin.kbs import admin_kb, task_kb, employee_kb
from taskbot.dao.dao import UserDAO
from taskbot.dao.session_maker import connection
from taskbot.admin.schemas import UserTelegramId

admin_router = Router()


@admin_router.message(Command("help"))
async def cmd_help(message: Message):
    logger.info("Вызов команды /help")
    await message.answer(
        f"Список комманд:"
    )


@admin_router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info("Вызов команды /start")
    await message.answer(
        f"👋🏻 Привет, {message.chat.id}!\nВыберите дальнейшие действия:",
        reply_markup=admin_kb()
    )


# @admin_router.message(Command("bot_stop"))
# async def cmd_stop(call: CallbackQuery):
#     logger.info("Вызов команды /stop")
#     await bot.close()


@admin_router.callback_query(F.data == "admin_panel")
@connection
async def admin_panel(call: CallbackQuery, session: AsyncSession):
    logger.info("Вызов команды /start_admin")
    
    user_id = call.from_user.id
    user = await UserDAO.find_one_or_none(session, UserTelegramId(telegram_id=user_id))

    if (user):
        await call.answer("Доступ в админ-панель разрешен!")
        return await call.message.edit_text(
            text=f"Выберите необходимое действие:",
            reply_markup=admin_kb()
        )

    await call.message.edit_text(
        text=f"У вас нет доступа к админ_панели!",
        reply_markup=None
    )


@admin_router.callback_query(F.data == 'role_menu')
async def role_menu(call: CallbackQuery):
    logger.info("Вызов команды /role_menu")

    


@admin_router.callback_query(F.data == "employee_menu")
async def employee_menu(call: CallbackQuery):
    logger.info("Вызов команды /employee_menu")
    await call.message.edit_text(
        text=f"Выберите действия с сотрудниками:",
        reply_markup=employee_kb()
    )


@admin_router.callback_query(F.data == "employee_list")
async def employee_list(call: CallbackQuery):
    logger.info("Вызов команды /employee_list")
    await call.message.edit_text(
        text=f"Список сотрудников:",
        reply_markup=None
    )


@admin_router.callback_query(F.data == "employee_add")
async def employee_add():
    logger.info("Вызов команды /employee_add")
    await bot.send_message(
        chat_id="", 
        text="Вас добавили как сотрудника"
    )
    

@admin_router.callback_query(F.data == "task_list")
async def task_list(call: CallbackQuery):
    logger.info("Вызов команды /tasks")
    await call.message.edit_text(
        text=f"Список задач:",
        reply_markup=None
    )


@admin_router.callback_query(F.data == "task_menu")
async def task_menu(call: CallbackQuery):
    logger.info("Вызов команды /task_menu")
    await call.message.edit_text(
        text=f"Выберите действия с задачами:",
        reply_markup=task_kb()
    )


@admin_router.callback_query(F.data == "send_messages")
async def send_messages(call: CallbackQuery):
    logger.info("Вызов команды /messages")
    await call.message.edit_text(
        text=f"Послать рассылку:",
        reply_markup=None
    )

