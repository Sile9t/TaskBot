import asyncio
from loguru import logger
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from config import bot
from taskbot.dao.dao import RoleDAO
from taskbot.admin.kbs import role_kb, role_list_kb

role_router = Router()

@role_router.message(Command('role_menu'))
async def role_menu(message: Message):
    logger.info("Вызов кнопки admin/role_menu")
    await message.answer(
        text=f"Меню должностей:",
        reply_markup=role_kb()
    )


@role_router.callback_query(F.data == 'role_menu')
async def role_menu(call: CallbackQuery):
    logger.info("Вызов кнопки admin/role_menu")
    await call.message.edit_text(
        text=f"Меню должностей:",
        reply_markup=role_kb()
    )


async def getPagesCount(session: AsyncSession, filters: BaseModel = None):
    rolesCount = await RoleDAO.count(session, filters)
    pagesCount = rolesCount / 5
    if (rolesCount % 5 > 0):
        pagesCount += 1

    return pagesCount


@role_router.message(F.text.startswith("role_list"))
async def role_list(message: Message, session_without_commit: AsyncSession):
    logger.info("Вызов команды admin/role_list")
    
    if (message.text.find('role_list_') > -1):
        page = int(message.text.replace('role_list_', ''))
    else:
        page = 1
    roles = await RoleDAO.find_all(session_without_commit)
    
    pagesCount = await getPagesCount(session_without_commit)
    
    data = (
        f'Список должностей:\n'
    )
    
    for role in roles:
        data += (
            f'ID: {role.id}\n'
            f'Название: {role.name}\n'
            f'Описание: {role.description}\n'
            f'\n'
        )
    
    await message.answer(
        text=data,
        reply_markup=await role_list_kb(page, pagesCount)
    )


@role_router.callback_query(F.data.startswith("role_list"))
async def role_list(call: CallbackQuery, session_without_commit: AsyncSession):
    logger.info("Вызов кнопки admin/role_list")

    await call.answer()
    if (call.data.find('role_list_') > -1):
        page = int(call.data.replace('role_list_', ''))
    else:
        page = 1
    roles = await RoleDAO.paginate(session_without_commit, page, 5)
    
    rolesCount = await RoleDAO.count(session_without_commit)
    pagesCount = rolesCount / 5
    if (rolesCount % 5 > 0):
        pagesCount += 1

    data = (
        f'Список должностей:\n'
    )
    
    logger.info('Составления списка должностей')
    for role in roles:
        data += (
            f'ID: {role.id}\n'
            f'Название: {role.name}\n'
            f'Описание: {role.description}\n'
            f'\n'
        )
    
    logger.info(f"Возврат списка должностей")
    async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action='typing'):
        await asyncio.sleep(2)
        await call.message.answer(
            text=data,
            reply_markup=role_list_kb(1, pagesCount)
        )


@role_router.callback_query(F.data == "role_add")
async def role_add(call: CallbackQuery):
    logger.info("Вызов кнопки admin/role_add")


@role_router.callback_query(F.data == "role_update")
async def role_update(call: CallbackQuery):
    logger.info("Вызов кнопки admin/role_update")


@role_router.callback_query(F.data == "role_delete")
async def role_delete(call: CallbackQuery):
    logger.info("Вызов кнопки admin/role_delete")
