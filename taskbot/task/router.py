from loguru import logger
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from taskbot.dao.models import User
from taskbot.task.state import TaskCreate, TaskRead, TaskUpdate, TaskDelete, TaskStatusUpdate, TaskPriorityUpdate, TaskRegionUpdate, TaskPerformersUpdate, TaskDatesUpdate
from taskbot.task.kbs import task_menu_kb, task_update_menu
from taskbot.admin.filters import PassUsersWithRoleIds

task_router = Router()


@task_router.message(Command('task_menu'))
async def task_menu(message: Message, auth: User):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов кнопки admin/task_menu")
    await message.answer(
        text=f"Меню для задач:",
        reply_markup=task_menu_kb(auth.role_id)
    )


@task_router.callback_query(F.data == 'task_menu')
async def task_menu(call: CallbackQuery, auth: User):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/task_menu")
    await call.message.edit_text(
        text=f"Меню для задач:",
        reply_markup=task_menu_kb(auth.role_id)
    )


@task_router.message(F.text.startswith("task_list"))
@task_router.callback_query(F.data.startswith("task_list"))
async def task_list(call: CallbackQuery, dialog_manager: DialogManager, auth: User):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/task_list")

    await call.answer()
    await dialog_manager.start(
        state=TaskRead.id,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_add", PassUsersWithRoleIds([1, 2]))
async def task_add(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/task_add\nЗапуск сценария добавления задачи")

    await call.answer("Добавление задачи")
    await dialog_manager.start(
        state=TaskCreate.title,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_update", PassUsersWithRoleIds([1, 2]))
async def task_update(call: CallbackQuery, dialog_manager: DialogManager, auth: User):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/task_update")

    await call.answer("Изменение задачи")
    await call.message.edit_text(
        text=f"Меню для изменения задачи",
        reply_markup=task_update_menu(auth.role_id)
    )


@task_router.callback_query(F.data == "task_full_update", PassUsersWithRoleIds([1, 2]))
async def task_full_update(call: CallbackQuery, dialog_manager: DialogManager, auth: User):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/task_full_update")

    await call.answer("Изменение задачи")
    await dialog_manager.start(
        state=TaskUpdate.id,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_dates_update")
async def task_dates_update(call: CallbackQuery, dialog_manager: DialogManager, auth: User):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/task_dates_update")

    await call.answer("Изменение дат задачи")
    await dialog_manager.start(
        state=TaskDatesUpdate.id,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_status_update")
async def task_status_update(call: CallbackQuery, dialog_manager: DialogManager, auth: User):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/task_status_update")

    await call.answer("Изменение статуса задачи")
    await dialog_manager.start(
        state=TaskStatusUpdate.id,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_priority_update", PassUsersWithRoleIds([1, 2]))
async def task_priority_update(call: CallbackQuery, dialog_manager: DialogManager, auth: User):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/task_priority_update")

    await call.answer("Изменение приоритета задачи")
    await dialog_manager.start(
        state=TaskPriorityUpdate.id,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_region_update", PassUsersWithRoleIds([1, 2]))
async def task_region_update(call: CallbackQuery, dialog_manager: DialogManager, auth: User):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/task_region_update")

    await call.answer("Изменение региона задачи")
    await dialog_manager.start(
        state=TaskRegionUpdate.id,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_set_performers", PassUsersWithRoleIds([1, 2]))
async def task_set_performers(call: CallbackQuery, dialog_manager: DialogManager, auth: User):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/task_set_performers")

    await call.answer("Назначение исполнителей")
    await dialog_manager.start(
        state=TaskPerformersUpdate.id,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_delete", PassUsersWithRoleIds([1, 2]))
async def task_delete(call: CallbackQuery, dialog_manager: DialogManager, auth: User):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов сценария удаления задачи")

    await call.answer("Удаление задачи")
    await dialog_manager.start(
        state=TaskDelete.id,
        mode=StartMode.RESET_STACK
    )
