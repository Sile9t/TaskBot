from loguru import logger
from datetime import date
from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedMultiselect

from ..dao.models import User
from ..dao.dao import TaskDAO, RegionDAO, RegionDAO, TaskPriorityDAO, UserDAO
from ..dao.schemas import TaskDtoBase
from ..admin.kbs import main_admin_kb
from ..admin.schemas import UserTelegramId
from ..task.kbs import task_menu_kb
from ..task.state import TaskCreate, TaskUpdate, TaskPerformersUpdate


async def go_menu(call: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    userRoleId = auth.role_id if auth else 3
    await call.answer("Сценарий отменен!")
    await call.message.answer(
        "Вы отменили сценарий. Меню для задач:",
        reply_markup=task_menu_kb(userRoleId)
    )

async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    userRoleId = auth.role_id if auth else 3
    await callback.answer("Сценарий отменен!")
    await callback.message.answer(
        "Вы отменили сценарий.", 
        reply_markup=main_admin_kb(userRoleId)
    )


async def on_task_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    task_id = int(dialog_manager.find("id").get_value())
    selected_task = await TaskDAO.find_one_or_none_by_id(session, task_id)

    dialog_manager.dialog_data["selected_task"] = selected_task
    await call.answer(f"Выбрана задача №{task_id}")
    await dialog_manager.next()


async def on_task_id_input_error(message: Message, dialog_: Any, dialog_manager: DialogManager, error_: ValueError, **kwargs):
    await message.answer("Номер должен быть числом!")


async def on_startline_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date, **kwargs):
    dialog_manager.dialog_data['startline'] = selected_date
    await call.answer(f"Выбранная дата: {str(selected_date)}")
    await dialog_manager.next()


async def on_deadline_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date, **kwargs):
    dialog_manager.dialog_data['deadline'] = selected_date
    await call.answer(f"Выбранная дата: {str(selected_date)}")
    await dialog_manager.next()


async def on_is_active_selected(call: CallbackQuery, widger, dialog_manager: DialogManager, is_active: bool, **kwargs):
    dialog_manager.dialog_data['is_active'] = str(is_active)
    logger.info(f"Is_active value: {is_active}")
    await dialog_manager.next()


async def on_performers_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    task_id = dialog_manager.find('id').get_value()
    task = await TaskDAO.find_one_or_none_by_id(session, task_id)

    if (task is None):
        await call.answer("Такой задачи не существует")
        return await dialog_manager.switch_to(TaskPerformersUpdate.id)

    caption = task.getPerformersCaption()
    await call.message.edit_text(
        text=f"Задаче {task.title} назначено {len(task.performers)} исполнителей",
        reply_markup=None
    )

    if (len(task.performers) > 0):
        notificationText = f"Вам назначили задачу#{task.id} <b>{task.title}</b>"
        performer_id = task.performers[0].telegram_id
        chatId = f"{performer_id}{performer_id}"
        await call.bot.send_message(performer_id,notificationText)

    await call.message.answer(f"Исполнители задачи:\n{caption}")
    await dialog_manager.done()


async def on_performer_state_change(call: CallbackQuery, select: ManagedMultiselect, dialog_manager: DialogManager, item: int, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")
    task_id = dialog_manager.find('id').get_value()
    task = await TaskDAO.find_one_or_none_by_id(session, task_id)
    user = await UserDAO.find_one_or_none_by_id(session, item)
    logger.info(f"Select item: {select.get_checked()}")
    logger.info(f"Select item is checked: {select.is_checked(item)}")
    logger.info(f"Item with changed state: {item}")


    if (select.is_checked(item)):
        task.performers.append(user)
    else:
        task.performers.remove(user)
    await session.commit()


async def on_create_confirmation(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get("session_with_commit")

    userRoleId = auth.role_id if auth else 3
    creator = await UserDAO.find_one_or_none(
        session,
        UserTelegramId(telegram_id=call.from_user.id)
    )
    title = dialog_manager.find('title').get_value()
    description = dialog_manager.find('description').get_value()
    startline = dialog_manager.dialog_data['startline']
    deadline = dialog_manager.dialog_data['deadline']
    is_active = dialog_manager.dialog_data['is_active']

    status_id = dialog_manager.dialog_data['status_id']
    status = await RegionDAO.find_one_or_none_by_id(session, status_id)
    if status is None:
        await call.message.answer("Такого статуса не существует!")
        return await dialog_manager.switch_to(TaskCreate.status)

    priority_id = dialog_manager.dialog_data['priority_id']
    priority = await TaskPriorityDAO.find_one_or_none_by_id(session, priority_id)
    if priority is None:
        await call.message.answer("Такого приоритета не существует!")
        return await dialog_manager.switch_to(TaskCreate.priority)

    region = dialog_manager.dialog_data['region']
    if region is None:
        await call.message.answer("Такого региона не существует!")
        return await dialog_manager.switch_to(TaskCreate.region)

    newTask = TaskDtoBase(
        title=title,
        description=description,
        startline=startline,
        deadline=deadline,
        is_active=is_active,
        status_id=status_id,
        priority_id=priority_id,
        region_id=region.id,
        creator_id=creator.id
    )

    check = await TaskDAO.find_one_or_none(session, newTask)
    if not check:
        await call.answer("Приступаю к сохранению")
        task = await TaskDAO.add(session, newTask)
        await call.answer(f"Задача успешно добавлена!")
        text = "Задача успешно добавлена"
        await call.message.answer(text, reply_markup=main_admin_kb(userRoleId))

        await dialog_manager.done()
        await session.commit()
    else:
        await call.message.answer("Эта задача уже существует!")
        await dialog_manager.back()

    
async def on_update_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get("session_with_commit")
    
    userRoleId = auth.role_id if auth else 3
    user_id = callback.from_user.id
    id = dialog_manager.find('id').get_value()
    title = dialog_manager.find('title').get_value()
    description = dialog_manager.find('description').get_value()
    startline = dialog_manager.dialog_data['startline']
    deadline = dialog_manager.dialog_data['deadline']
    is_active = dialog_manager.dialog_data['is_active']

    status_id = dialog_manager.dialog_data['status_id']
    status = await RegionDAO.find_one_or_none_by_id(session, status_id)
    if status is None:
        await callback.message.answer("Такого статуса не существует!")
        return await dialog_manager.switch_to(TaskCreate.status)

    priority_id = dialog_manager.dialog_data['priority_id']
    priority = await TaskPriorityDAO.find_one_or_none_by_id(session, priority_id)
    if priority is None:
        await callback.message.answer("Такого приоритета не существует!")
        return await dialog_manager.switch_to(TaskCreate.priority)

    region_id = dialog_manager.dialog_data['region_id']
    region = await RegionDAO.find_one_or_none_by_id(session, region_id)
    if region is None:
        await callback.message.answer("Такого региона не существует!")
        return await dialog_manager.switch_to(TaskCreate.region)
    
    check = await TaskDAO.find_one_or_none_by_id(session, id)
    if check:
        await callback.answer("Сохранение")

        check.title = title
        check.description = description
        check.startline = startline
        check.deadline = deadline
        check.is_active = eval(is_active)
        check.status_id = status_id
        check.priority_id = priority_id
        check.region_id = region_id

        confirmText = f"Запись задачи#{check.id} \"{check.title}\" успешно обновлена!"
        logger.info(confirmText)
        await callback.answer(confirmText)
        await callback.message.answer(confirmText, reply_markup=main_admin_kb(userRoleId))

        await dialog_manager.done()
    else:
        await callback.message.answer("Запись задачи не найдена!")
        await dialog_manager.switch_to(TaskUpdate.id)


async def process_delete_task(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get("session_with_commit")

    userRoleId = auth.role_id if auth else 3
    id = dialog_manager.find("id").get_value()
    task = await TaskDAO.find_one_or_none_by_id(session, id)
    
    if task:
        await call.answer("Удаление записи")
        taskDto = TaskDtoBase(
            title=task.title,
            description=task.description,
            startline=task.startline,
            deadlline=task.deadline,
            is_active=task.is_active,
            status_id=task.status_id,
            priority_id=task.priority_id,
            region_id=task.region_id,
            creator_id=task.creator_id
        )
        count = await TaskDAO.delete(session, taskDto)
        text = f"Удалено {count} записей"
        await session.commit()
        await call.message.answer(
            text,
            reply_markup=main_admin_kb(userRoleId)
        )
        
        await dialog_manager.done()
    else:
        await call.answer("Запись задачи не найдена!\nВведите другой id.")


async def on_status_change_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get("session_without_commit")
    
    userRoleId = auth.role_id if auth else 3
    user_id = call.from_user.id
    id = dialog_manager.find('id').get_value()

    status_id = int(item_id)
    selected_status = await RegionDAO.find_one_or_none_by_id(session, status_id)
    if (selected_status is None):
        return call.answer(f"Выбраная запись №{status_id} не существует. Выберите еще раз")
    
    check = await TaskDAO.find_one_or_none_by_id(session, id)
    if check:
        await call.answer("Сохранение")

        check.status_id = status_id
        
        await session.commit()

        await call.answer(f"Запись задачи успешно обновлена!")
        text = "Запись задачи успешно сохранена"
        await call.message.answer(text, reply_markup=main_admin_kb(userRoleId))

        await dialog_manager.done()
    else:
        await call.message.answer("Запись задачи не найдена!")
        await dialog_manager.switch_to(TaskUpdate.status)


async def on_priority_change_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get("session_without_commit")

    userRoleId = auth.role_id if auth else 3
    user_id = call.from_user.id
    id = dialog_manager.find('id').get_value()

    priority_id = int(item_id)
    selected_priority = await TaskPriorityDAO.find_one_or_none_by_id(session, priority_id)
    if (selected_priority is None):
        return call.answer(f"Выбраная запись №{priority_id} не существует. Выберите еще раз")
    
    check = await TaskDAO.find_one_or_none_by_id(session, id)
    if check:
        await call.answer("Сохранение")

        check.priority_id = priority_id
        
        await session.commit()

        await call.answer(f"Запись задачи успешно обновлена!")
        text = "Запись задачи успешно сохранена"
        await call.message.answer(text, reply_markup=main_admin_kb(userRoleId))

        await dialog_manager.done()
    else:
        await call.message.answer("Запись задачи не найдена!")
        await dialog_manager.switch_to(TaskUpdate.priority)


async def on_region_change_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get("session_without_commit")

    userRoleId = auth.role_id if auth else 3
    user_id = call.from_user.id
    id = dialog_manager.find('id').get_value()

    region_id = int(item_id)
    selected_region = await RegionDAO.find_one_or_none_by_id(session, region_id)
    if (selected_region is None):
        return call.answer(f"Выбраная запись №{region_id} не существует. Выберите еще раз")
    
    check = await TaskDAO.find_one_or_none_by_id(session, id)
    if check:
        await call.answer("Сохранение")

        check.region_id = region_id
        
        await session.commit()

        await call.answer(f"Запись задачи успешно обновлена!")
        text = "Запись задачи успешно сохранена"
        await call.message.answer(text, reply_markup=main_admin_kb(userRoleId))

        await dialog_manager.done()
    else:
        await call.message.answer("Запись задачи не найдена!")
        await dialog_manager.switch_to(TaskUpdate.region)

async def on_dates_change_confirmation(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get("session_without_commit")
    
    userRoleId = auth.role_id if auth else 3
    user_id = call.from_user.id
    id = dialog_manager.find('id').get_value()

    startline = dialog_manager.dialog_data['startline']
    deadline = dialog_manager.dialog_data['deadline']

    check = await TaskDAO.find_one_or_none_by_id(session, id)
    if check:
        await call.answer("Сохранение")

        check.startline = startline
        check.deadline = deadline
        
        await session.commit()

        await call.answer(f"Запись задачи успешно обновлена!")
        text = "Запись задачи успешно сохранена"
        await call.message.answer(text, reply_markup=main_admin_kb(userRoleId))

        await dialog_manager.done()
    else:
        await call.message.answer("Запись задачи не найдена!")
        await dialog_manager.switch_to(TaskUpdate.status)
