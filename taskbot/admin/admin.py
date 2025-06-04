import asyncio
from datetime import datetime, timedelta
from loguru import logger
from typing import List
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, Message, ChatJoinRequest
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.admin.kbs import main_admin_kb
from taskbot.dao.models import User
from taskbot.dao.dao import UserDAO, RoleDAO
from taskbot.dao.schemas import UserDtoBase, RoleDto
from taskbot.admin.schemas import UserTelegramId, UserRoleId
from taskbot.admin.filters import IsAdmin


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
admin_router.message.filter(IsAdmin)


@admin_router.message(Command("help"))
async def cmd_help(message: Message):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов команды admin/help")
    await message.answer(
        f"Список комманд:",
        reply_markup=None
    )


@admin_router.message(CommandStart())
async def cmd_start(message: Message, session_with_commit: AsyncSession):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов команды admin/start")
    
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


@admin_router.message(Command('admin_panel'))
async def admin_panel(message: Message, session_without_commit: AsyncSession):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов команды admin/admin_panel")

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
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов кнопки admin/admin_panel")
    
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


@admin_router.message(Command('refer_link'))
async def refer_link(message: Message):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Command - admin/refer_link")

    if (message.chat.type == 'private'):
        return await message.answer(
            "Приглашения работают только для открытых чатов. Сделайте свой чат открытым, если вы хотите воспользоваться этой функцией. Если вы общаетесь с ботом в личном чате - создайте групповой открытый чат и добавьте этого бота как администратора."
        )
    
    chat_id = message.chat.id
    expire_date = datetime.now() + timedelta(days=1)
    try:
        invite_link_obj = await message.bot.create_chat_invite_link(
            chat_id=chat_id,
            expire_date=expire_date.timestamp(),
            member_limit=1
        )
        #TODO: add invite link to database for revoke passibility
        
        invite_link = invite_link_obj.invite_link
    except Exception as e:        
        return message.answer(
            text=e.message
        )
    
    text = (f"Ссылка-приглашение:\n"
            f"🔗 <code>{invite_link}</code> (нажмите чтобы скопировать)\n"
            f"Отправьте ее пользователю, которого вы хотите добавить в чат как сотрудника\n"
            f"❗ (Работает в течение суток для 1 пользователя)"
    )

    await message.answer(
        text=text,
        reply_markup=None
    )


@admin_router.message(Command('cancel_all_refer_links'))
async def cancel_all_refer_links(message: Message):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Command - admin/cancel_all_refer_links")
    #TODO: get all invite link for user, revoke them all and delete from db
    message.bot.revoke_chat_invite_link()


#TODO:
# #
# Message routes
# #
@admin_router.callback_query(F.data == "send_messages")
async def send_messages(call: CallbackQuery):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/messages")
    await call.message.edit_text(
        text=f"Послать рассылку:",
        reply_markup=None
    )

