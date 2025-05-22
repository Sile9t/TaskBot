import asyncio
from typing import Dict, Any
from loguru import logger
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import DialogManager, StartMode
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.region.kbs import region_menu_kb
from taskbot.region.state import RegionCreate, RegionRead, RegionUpdate, RegionDelete

region_router = Router()

@region_router.message(Command('region_menu'))
async def region_menu(message: Message):
    logger.info("Вызов команды admin/region_menu")
    await message.answer(
        text=f"Меню для регионов:",
        reply_markup=region_menu_kb()
    )


@region_router.callback_query(F.data == "region_menu")
async def region_menu(call: CallbackQuery):
    logger.info("Вызов кнопки admin/region_menu")
    await call.message.answer(
        text=f"Меню для регионов:",
        reply_markup=region_menu_kb()
    )


@region_router.callback_query(F.data == "region_list")
async def region_list(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/region_list")

    await call.answer()
    
    await dialog_manager.start(
        state=RegionRead.id,
        mode=StartMode.RESET_STACK
    )


@region_router.callback_query(F.data == "region_create")
async def region_create(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/region_create")

    await call.answer("Сценарий добавления")
    await dialog_manager.start(
        state=RegionCreate.name,
        mode=StartMode.RESET_STACK
    )


@region_router.callback_query(F.data == 'region_update')
async def region_update(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/region_update")

    await call.answer("Сценарий изменения")
    await dialog_manager.start(
        state=RegionUpdate.id,
        mode=StartMode.RESET_STACK
    )


@region_router.callback_query(F.data == 'region_delete')
async def region_delete(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/region_delete")

    await call.answer("Сценарий удаления")
    await dialog_manager.start(
        state=RegionDelete.id,
        mode=StartMode.RESET_STACK
    )