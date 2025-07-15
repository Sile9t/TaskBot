from loguru import logger
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from ..admin.kbs import main_admin_kb
from ..dao.dao import UserDAO, RoleDAO
from ..dao.schemas import UserDtoBase
from ..admin.schemas import UserTelegramId, UserRoleId
from ..dao.models import User

async def getAdminFromMessage(message: Message, session_without_commit: AsyncSession):
    return UserDtoBase(
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name if message.from_user.last_name is not None else "Нет фамилии",
        telegram_id=message.from_user.id,
        role_id=1,
        region_id=1
    )

async def getEmployeeFromMessage(message: Message, session_without_commit: AsyncSession):
    return UserDtoBase(
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name if message.from_user.last_name is not None else "Нет фамилии",
        telegram_id=message.from_user.id,
        role_id=3,
        region_id=None
    )


general_router = Router()

@general_router.message(Command("help") | F.data == "/help")
async def cmd_help(message: Message):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов команды admin/help")
    await message.answer(
        f"Список комманд:",
        reply_markup=None
    )


@general_router.message(CommandStart())
async def cmd_start(message: Message, session_with_commit: AsyncSession, command: CommandObject = None, auth: User|None = None):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов команды admin/start")
    
    return await message.answer(
        f"👋🏻 Привет, {message.from_user.full_name}!\nВы зарегистрированы как {auth.role.name}.",
        reply_markup=main_admin_kb(auth.role_id)
    )
