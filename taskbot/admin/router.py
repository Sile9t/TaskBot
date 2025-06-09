import asyncio
from datetime import datetime, timedelta
from loguru import logger
from typing import List
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import CallbackQuery, Message, ChatJoinRequest
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.admin.kbs import main_admin_kb
from taskbot.dao.models import User
from taskbot.dao.dao import UserDAO, RoleDAO, ReferDAO
from taskbot.dao.schemas import UserDtoBase, RoleDto, ReferDtoBase
from taskbot.admin.schemas import UserTelegramId, UserRoleId, ReferLinkFilterByChatAndUserIds
from taskbot.admin.filters import IsAdmin


admin_router = Router()
admin_router.message.filter(IsAdmin)


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
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/admin_panel")
    
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

#deprecated
{
# @admin_router.message(Command('refer_link'))
# async def refer_link(message: Message, session_with_commit: AsyncSession):
#     logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Command - admin/refer_link")

#     if (message.chat.type == 'private'):
#         return await message.answer(
#             "Приглашения работают только для открытых чатов. Сделайте свой чат открытым, если вы хотите воспользоваться этой функцией. Если вы общаетесь с ботом в личном чате - создайте групповой открытый чат и добавьте этого бота как администратора."
#         )
    
#     chat_id = message.chat.id
#     expire_date = datetime.now() + timedelta(days=1)
#     try:
#         invite_link_obj = await message.bot.create_chat_invite_link(
#             chat_id=chat_id,
#             expire_date=expire_date.timestamp(),
#             member_limit=1
#         )

#         invite_link = invite_link_obj.invite_link
        
#         referDto = ReferDtoBase(
#             chat_id=message.chat.id,
#             user_id=message.from_user.id,
#             link=invite_link
#         )
#         await ReferDAO.add(session_with_commit, referDto)
#     except Exception as e:        
#         return message.answer(
#             text=e.message
#         )
    
#     text = (f"Ссылка-приглашение:\n"
#             f"🔗 <code>{invite_link}</code> (нажмите чтобы скопировать)\n"
#             f"Отправьте ее пользователю, которого вы хотите добавить в чат как сотрудника\n"
#             f"❗ (Работает в течение суток для 1 пользователя)"
#     )

#     await message.answer(
#         text=text,
#         reply_markup=None
#     )
}


#deprecated
{  
# @admin_router.message(Command('cancel_all_refer_links'))
# async def cancel_all_refer_links(message: Message, session_with_commit: AsyncSession):
#     logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Command - admin/cancel_all_refer_links")
#     chat_id = message.chat.id
#     user_id = message.chat.id

#     refers = await ReferDAO.find_all(
#         session_with_commit,
#         ReferLinkFilterByChatAndUserIds(
#             chat_id=chat_id,
#             user_id=user_id
#         )
#     )
#     for refer in refers:
#         #TODO: did not work
#         await message.bot.revoke_chat_invite_link(chat_id, refer.link)
    
#     await message.answer(
#         text="Все ссылки-приглашения от бота были удалены."
#     )
}


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

