import asyncio
import re
from loguru import logger
from typing import List
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender
from config import bot
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import create_model
from taskbot.admin.kbs import admin_kb, task_kb, role_kb, role_list_kb, employee_kb
from taskbot.dao.session_maker import connection
from taskbot.dao.dao import UserDAO, RoleDAO
from taskbot.dao.schemas import UserDto, RoleDto
from taskbot.admin.schemas import UserTelegramId, UserRoleId

async def addAdmin(message: Message, session_without_commit: AsyncSession):
    role = await RoleDAO.find_one_or_none_by_id(session_without_commit, 1)
    return UserDto(
        first_name=message.from_user.first_name,
        second_name=message.from_user.last_name,
        telegram_id=message.from_user.id,
        role_id=1,
        role=role
    )

async def addEmployee(message: Message, session_without_commit: AsyncSession):
    role = await RoleDAO.find_one_or_none_by_id(session_without_commit, 3)
    return UserDto(
        first_name=message.from_user.first_name,
        second_name=message.from_user.last_name,
        telegram_id=message.from_user.id,
        role_id=3,
        role=role
    )


admin_router = Router()


@admin_router.message(Command("help"))
async def cmd_help(message: Message):
    logger.info("Вызов команды admin/help")
    await message.answer(
        f"Список комманд:",
        reply_markup=None
    )


@admin_router.message(CommandStart())
async def cmd_start(message: Message, session_without_commit: AsyncSession):
    logger.info("Вызов команды admin/start")
    
    filterModel = UserRoleId(role_id=1)
    admins = await UserDAO.find_all(session_without_commit, filterModel)

    # if (admins.count == 0):
    #     role = await RoleDAO.find_one_or_none_by_id(session, 1)
    #     newUser = UserDto(
    #         first_name=message.from_user.first_name,
    #         second_name=message.from_user.last_name,
    #         telegram_id=message.from_user.id,
    #         role_id=1,
    #         role=role
    #     )
    # else:
    #     role = await RoleDAO.find_one_or_none_by_id(session, 3)
    #     newUser = UserDto(
    #         first_name=message.from_user.first_name,
    #         second_name=message.from_user.last_name,
    #         telegram_id=message.from_user.id,
    #         role_id=3,
    #         role=role
    #     )

    # await UserDAO.add(session, newUser)
    # session_without_commit.commit()
    
    for admin in admins:
        if (admin.telegram_id == message.from_user.id):
            return await message.answer(
                f"👋🏻 Привет, {message.from_user.full_name}!\nВы не зарегистрированы",
                reply_markup=None
            )

    # await message.answer(
    #     f"👋🏻 Привет, {message.from_user.full_name}!\nВы зарегистрированы как {role.name}",
    #     reply_markup=admin_kb()
    # )


# @admin_router.message(Command("bot_stop"))
# async def cmd_stop(call: CallbackQuery):
#     logger.info("Вызов команды /stop")
#     await bot.close()


@admin_router.message(Command('admin_panel'))
async def admin_panel(message: Message, session_without_commit: AsyncSession):
    logger.info("Вызов команды admin/admin_panel")

    user_id = message.from_user.id
    user = await UserDAO.find_one_or_none(session_without_commit, UserTelegramId(telegram_id=user_id))
    
    if (user):
        return await message.answer(
            text=f"Выберите необходимое действие:",
            reply_markup=admin_kb()
        )
    
    await message.answer(
        text=f"У вас нет доступа к админ-панели!",
        reply_markup=None
    )


@admin_router.callback_query(F.data == "admin_panel")
async def admin_panel(call: CallbackQuery, session_without_commit: AsyncSession):
    logger.info("Вызов кнопки admin/admin_panel")
    
    user_id = call.from_user.id
    user = await UserDAO.find_one_or_none(session_without_commit, UserTelegramId(telegram_id=user_id))

    if (user):
        await call.answer("Доступ в админ-панель разрешен!")
        return await call.message.edit_text(
            text=f"Выберите необходимое действие:",
            reply_markup=admin_kb()
        )

    await call.message.edit_text(
        text=f"У вас нет доступа к админ-панели!",
        reply_markup=None
    )

# #
# Employee routes
# #
@admin_router.message(Command("employee_menu"))
async def employee_menu(message: Message):
    logger.info("Вызов кнопки admin/employee_menu")
    await message.answer(
        text=f"Меню для сотрудников:",
        reply_markup=employee_kb()
    )


@admin_router.callback_query(F.data == "employee_menu")
async def employee_menu(call: CallbackQuery):
    logger.info("Вызов кнопки admin/employee_menu")
    await call.message.edit_text(
        text=f"Выберите действия с сотрудниками:",
        reply_markup=employee_kb()
    )


@admin_router.callback_query(F.data == "employee_list")
async def employee_list(call: CallbackQuery, session_without_commit: AsyncSession):
    logger.info("Вызов кнопки admin/employee_list")
    
    employees = await UserDAO.find_all(session_without_commit, UserRoleId(role_id=3))

    data = (
        f"Список сотрудников:\n"
    )

    for employee in employees:
        data += (
            f"{employee}\n"
        )
        
    await call.message.edit_text(
        text=f"Список сотрудников:",
        reply_markup=None
    )


@admin_router.callback_query(F.data == "employee_add")
async def employee_add():
    logger.info("Вызов кнопки admin/employee_add")
    await bot.send_message(
        chat_id="", 
        text="Вас добавили как сотрудника"
    )
    

# #
# Task routes
# #
@admin_router.message(Command("task_menu"))
async def task_menu(message: Message):
    logger.info("Вызов кнопки admin/task_menu")
    await message.answer(
        text=f"Меню для задач:",
        reply_markup=task_kb()
    )


@admin_router.callback_query(F.data == "task_menu")
async def task_menu(call: CallbackQuery):
    logger.info("Вызов кнопки admin/task_menu")
    await call.message.edit_text(
        text=f"Выберите действия с задачами:",
        reply_markup=task_kb()
    )


@admin_router.callback_query(F.data == "task_list")
async def task_list(call: CallbackQuery):
    logger.info("Вызов кнопки admin/task_list")
    await call.message.edit_text(
        text=f"Список задач:",
        reply_markup=None
    )


# #
# Message routes
# #
@admin_router.callback_query(F.data == "send_messages")
async def send_messages(call: CallbackQuery):
    logger.info("Вызов кнопки admin/messages")
    await call.message.edit_text(
        text=f"Послать рассылку:",
        reply_markup=None
    )

