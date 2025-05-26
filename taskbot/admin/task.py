import asyncio
from loguru import logger
from typing import List
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from config import bot
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from taskbot.admin.kbs import main_admin_kb, task_kb, employee_kb
from taskbot.dao.dao import UserDAO, RoleDAO
from taskbot.dao.schemas import UserDtoBase, RoleDto
from taskbot.admin.schemas import UserTelegramId, UserRoleId
from taskbot.task.state import TaskForm

task_router = Router()

@task_router.message(Command("task_menu"))
async def task_menu(message: Message, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/task_menu")
    # await message.answer(
    #     text=f"Меню для задач:",
    #     reply_markup=task_kb()
    # )

    await dialog_manager.start(
        state=TaskForm.list,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_menu")
async def task_menu(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/task_menu")
    # await call.message.edit_text(
    #     text=f"Выберите действия с задачами:",
    #     reply_markup=task_kb()
    # )

    await dialog_manager.start(
        state=TaskForm.list,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_list")
async def task_list(call: CallbackQuery):
    logger.info("Вызов кнопки admin/task_list")
    await call.message.edit_text(
        text=f"Список задач:",
        reply_markup=None
    )
