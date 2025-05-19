import asyncio
from loguru import logger
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, Message
from config import bot
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.admin.kbs import employee_kb, employee_list_kb
from taskbot.dao.dao import UserDAO
from taskbot.admin.schemas import UserRoleId

employee_router = Router()

@employee_router.message(Command("employee_menu"))
async def employee_menu(message: Message):
    logger.info("Вызов команды admin/employee_menu")
    await message.answer(
        text=f"Меню для сотрудников:",
        reply_markup=employee_kb()
    )


@employee_router.callback_query(F.data == "employee_menu")
async def employee_menu(call: CallbackQuery):
    logger.info("Вызов кнопки admin/employee_menu")
    await call.message.edit_text(
        text=f"Выберите действия с сотрудниками:",
        reply_markup=employee_kb()
    )


async def getPagesCount(session: AsyncSession, filters: BaseModel = None):
    rolesCount = await UserDAO.count(session, filters)
    pagesCount = rolesCount / 5
    if (rolesCount % 5 > 0):
        pagesCount += 1

    return pagesCount

@employee_router.callback_query(F.data == "employee_list")
async def employee_list(call: CallbackQuery, session_without_commit: AsyncSession):
    logger.info("Вызов кнопки admin/employee_list")
    
    if (call.message.text.find('role_list_') > -1):
        page = int(call.message.text.replace('role_list_', ''))
    else:
        page = 1
    employees = await UserDAO.find_all(session_without_commit, UserRoleId(role_id=3))

    pagesCount = await getPagesCount(session_without_commit)

    data = (
        f"Список сотрудников:\n"
    )

    for employee in employees:
        data += (
            f"{employee}\n"
        )
        
    await call.message.answer(
        text=data,
        reply_markup=await employee_list_kb(page, pagesCount)
    )


@employee_router.callback_query(F.data == "employee_add")
async def employee_add():
    logger.info("Вызов кнопки admin/employee_add")
    await bot.send_message(
        chat_id="", 
        text="Вас добавили как сотрудника"
    )
