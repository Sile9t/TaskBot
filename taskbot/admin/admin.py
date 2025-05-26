import asyncio
from loguru import logger
from typing import List
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from pydantic import BaseModel
from sqlalchemy.orm import lazyload
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.admin.kbs import main_admin_kb, task_kb, employee_kb
from taskbot.dao.models import User
from taskbot.dao.dao import UserDAO, RoleDAO
from taskbot.dao.schemas import UserDtoBase, RoleDto
from taskbot.admin.schemas import UserTelegramId, UserRoleId

async def getAdminFromMessage(message: Message, session_without_commit: AsyncSession):
    role = await RoleDAO.find_one_or_none_by_id(session_without_commit, 1)
    return UserDtoBase(
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        telegram_id=message.from_user.id,
        role_id=1,
        region_id=None
    )

async def getEmployeeFromMessage(message: Message, session_without_commit: AsyncSession):
    role = await RoleDAO.find_one_or_none_by_id(session_without_commit, 3)
    return UserDtoBase(
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        telegram_id=message.from_user.id,
        role_id=3,
        region_id=None
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
async def cmd_start(message: Message, session_with_commit: AsyncSession):
    logger.info("Вызов команды admin/start")
    
    tgIdFilter = UserTelegramId(
        telegram_id=message.from_user.id
    )
    check = await UserDAO.find_one_or_none(session_with_commit, tgIdFilter)
    
    if check is None:
        filterModel = UserRoleId(role_id=1)
        admins = await UserDAO.find_all(session_with_commit, filterModel)

        logger.info(
            f"\n\tUser:\n"
            f"\t\t{message.from_user.first_name}\n"
            f"\t\t{message.from_user.last_name}\n"
            f"\t\t{message.from_user.id}\n"
        )
        
        if (admins.count == 0):
            newUser = await getAdminFromMessage(message, session_with_commit)
        else:
            newUser = await getEmployeeFromMessage(message, session_with_commit)

        await UserDAO.add(session_with_commit, newUser)
        
        for admin in admins:
            if (admin.telegram_id == message.from_user.id):
                return await message.answer(
                    f"Пользователь {message.from_user.full_name} зарегистрирован!",
                    reply_markup=None
                )
        
        return await message.answer(
            f"👋🏻 Привет, {message.from_user.full_name}!\nВы не зарегистрированы",
            reply_markup=None
        )

    await message.answer(
        f"👋🏻 Привет, {message.from_user.full_name}!\nВы зарегистрированы как {check.role.name}",
        reply_markup=main_admin_kb()
    )


@admin_router.message(Command('admin_panel'))
async def admin_panel(message: Message, session_without_commit: AsyncSession):
    logger.info("Вызов команды admin/admin_panel")

    user_id = message.from_user.id
    user = await UserDAO.find_one_or_none(session_without_commit, UserTelegramId(telegram_id=user_id))
    
    if (user.role_id == 1):
        return await message.answer(
            text=f"Выберите необходимое действие:",
            reply_markup=main_admin_kb()
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

    if (user.role_id == 1):
        await call.answer("Доступ в админ-панель разрешен!")
        return await call.message.edit_text(
            text=f"Выберите необходимое действие:",
            reply_markup=main_admin_kb()
        )

    await call.message.edit_text(
        text=f"У вас нет доступа к админ-панели!",
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

