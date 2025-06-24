from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from taskbot.dao.dao import RegionDAO
from taskbot.region.kbs import region_menu_kb
from taskbot.region.state import RegionCreate, RegionRead, RegionUpdate, RegionDelete, RegionWireChat
from .shemas import RegionChatIdFilter
from ..admin.filters import IsAdmin

region_router = Router()
region_router.message.filter(IsAdmin())

@region_router.message(Command('region_menu'))
async def region_menu(message: Message):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов команды admin/region_menu")
    await message.answer(
        text=f"Меню для регионов:",
        reply_markup=region_menu_kb()
    )


@region_router.callback_query(F.data == "region_menu")
async def region_menu(call: CallbackQuery):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/region_menu")
    await call.message.answer(
        text=f"Меню для регионов:",
        reply_markup=region_menu_kb()
    )


@region_router.message(Command('wire_chat_status'))
async def wire_chat_status(message: Message, session_without_commit: AsyncSession):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов кнопки admin/wire_chat_status")
    chatId = message.chat.id

    if (chatId != message.from_user.id):
        region = await RegionDAO.find_one_or_none(session_without_commit, RegionChatIdFilter(chat_id=chatId))
        if region:
            await message.answer(
                text=f"Чат привязан к {region.name}"
            )
        else:
            await message.answer(
                text=f"Чат не привязан ни к какому региону"
            )
    else:
        await message.answer(
            text="Нельзя привязать/отвязать личный чат к региону"
        )


@region_router.message(Command('wire_chat'))
async def wire_chat(message: Message, dialog_manager: DialogManager):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов кнопки admin/wire_chat")
    chatId = message.chat.id

    if (chatId != message.from_user.id):
        await dialog_manager.start(
            state=RegionWireChat.id,
            mode=StartMode.RESET_STACK
        )
    else:
        await message.answer(
            text="Нельзя привязать/отвязать личный чат к региону"
        )


@region_router.message(Command('unwire_chat'))
async def wire_chat_status(message: Message, session_with_commit: AsyncSession):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов кнопки admin/wire_chat_status")
    chatId = message.chat.id

    if (chatId != message.from_user.id):
        region = await RegionDAO.find_one_or_none(session_with_commit, RegionChatIdFilter(chat_id=chatId))
        if region:
            region.chat_id = None

            await message.answer(
                text=f"Чат отвязан от {region.name}"
            )
        else:
            await message.answer(
                text=f"Чат не привязан ни к какому региону"
            )
    else:
        await message.answer(
            text="Нельзя привязать/отвязать личный чат к региону"
        )


@region_router.callback_query(F.data == "region_list")
async def region_list(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/region_list")

    await call.answer()
    
    await dialog_manager.start(
        state=RegionRead.id,
        mode=StartMode.RESET_STACK
    )


@region_router.callback_query(F.data == "region_create")
async def region_create(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/region_create")

    await call.answer("Сценарий добавления")
    await dialog_manager.start(
        state=RegionCreate.name,
        mode=StartMode.RESET_STACK
    )


@region_router.callback_query(F.data == 'region_update')
async def region_update(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/region_update")

    await call.answer("Сценарий изменения")
    await dialog_manager.start(
        state=RegionUpdate.id,
        mode=StartMode.RESET_STACK
    )


@region_router.callback_query(F.data == 'region_delete')
async def region_delete(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/region_delete")

    await call.answer("Сценарий удаления")
    await dialog_manager.start(
        state=RegionDelete.id,
        mode=StartMode.RESET_STACK
    )