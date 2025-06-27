from loguru import logger
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from ..admin.kbs import main_admin_kb
from ..dao.dao import UserDAO, RoleDAO
from ..dao.schemas import UserDtoBase
from ..admin.schemas import UserTelegramId, UserRoleId

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
async def cmd_start(message: Message, session_with_commit: AsyncSession, command: CommandObject = None):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов команды admin/start")
    
    tgIdFilter = UserTelegramId(
        telegram_id=message.from_user.id
    )
    check = await UserDAO.find_one_or_none(session_with_commit, tgIdFilter)
    
    if check is None:
        filterModel = UserRoleId(role_id=1)
        admins = await UserDAO.find_all(session_with_commit, filterModel)
        logger.info("Admins:", admins)

        if (len(admins) == 0):
            newUser = await getAdminFromMessage(message, session_with_commit)
        else:
            newUser = await getEmployeeFromMessage(message, session_with_commit)

        await UserDAO.add(session_with_commit, newUser)
        
        for admin in admins:
            if (admin.telegram_id == message.from_user.id):
                return await message.answer(
                    f"Сотрудник {message.from_user.full_name} зарегистрирован.",
                    reply_markup=None
                )
        
        userRole = await RoleDAO.find_one_or_none_by_id(session_with_commit, newUser.role_id)

        return await message.answer(
            f"👋🏻 Привет, {message.from_user.full_name}!\nВы зарегистрированы как {userRole.name}.",
            reply_markup=None
        )

    await message.answer(
        f"👋🏻 Привет, {message.from_user.full_name}!\nВы зарегистрированы как {check.role.name}.",
        reply_markup=main_admin_kb()
    )

