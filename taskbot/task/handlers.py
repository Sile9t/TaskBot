from loguru import logger
from datetime import date
from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from taskbot.dao.dao import TaskDAO, RegionDAO, TaskStatusDAO, TaskPriorityDAO
from taskbot.dao.schemas import TaskDto, TaskDtoBase
from taskbot.admin.kbs import main_admin_kb
from taskbot.task.kbs import task_menu_kb
from taskbot.task.state import TaskCreate, TaskUpdate

async def go_menu(call: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await call.answer("Сценарий отменен!")
    await call.message.answer(
        "Вы отменили сценарий. Меню для задач:",
        reply_markup=task_menu_kb()
    )

async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.answer("Сценарий отменен!")
    await callback.message.answer(
        "Вы отменили сценарий.", 
        reply_markup=main_admin_kb(callback.from_task.id)
    )


async def on_task_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    session = dialog_manager.middleware_data.get("session_without_commit")
    task_id = int(item_id)
    selected_task = await TaskDAO(session).find_one_or_none_by_id(task_id)

    dialog_manager.dialog_data["selected_task"] = selected_task
    await call.answer(f"Выбрана должность №{task_id}")
    await dialog_manager.next()


async def on_task_id_input_error(message: Message, dialog_: Any, dialog_manager: DialogManager, error_: ValueError):
    await message.answer("Номер должен быть числом!")

{
# async def on_task_id_input(message: Message, dialog_: Any, dialog_manager: DialogManager):
#     session = dialog_manager.middleware_data.get("session_without_commit")

#     id = dialog_manager.find('id').get_value()
#     task = await TaskDAO.find_one_or_none_by_id(session, id)

#     if task is None:
#         await message.answer(f"Должности с таким номером не существует!\nВведите его еще раз.")
#         return
    
#     await dialog_manager.next()
}

async def on_startline_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date):
    dialog_manager.dialog_data['startline'] = selected_date
    await call.answer(f"Выбранная дата: {str(selected_date)}")
    await dialog_manager.next()


async def on_deadline_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date):
    dialog_manager.dialog_data['deadline'] = selected_date
    await call.answer(f"Выбранная дата: {str(selected_date)}")
    await dialog_manager.next()


async def on_is_active_selected(call: CallbackQuery, widger, dialog_manager: DialogManager, is_active: bool):
    dialog_manager.dialog_data['is_active'] = str(is_active)
    logger.info(f"Is_active value: {is_active}")
    await dialog_manager.next()


async def on_create_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    user_id = callback.from_user.id
    title = dialog_manager.find('title').get_value()
    description = dialog_manager.find('description').get_value()
    startline = dialog_manager.dialog_data['startline']
    deadline = dialog_manager.dialog_data['deadline']
    is_active = dialog_manager.dialog_data['is_active']

    status_id = dialog_manager.find('status_id').get_value()
    status = await TaskStatusDAO.find_one_or_none_by_id(session, status_id)
    if status is None:
        await callback.message.answer("Такого статуса не существует!")
        return await dialog_manager.switch_to(TaskCreate.status)

    priority_id = dialog_manager.find('priority_id').get_value()
    priority = await TaskPriorityDAO.find_one_or_none_by_id(session, priority_id)
    if priority is None:
        await callback.message.answer("Такого приоритета не существует!")
        return await dialog_manager.switch_to(TaskCreate.priority)

    region_id = dialog_manager.find('region_id').get_value()
    region = await RegionDAO.find_one_or_none_by_id(session, region_id)
    if region is None:
        await callback.message.answer("Такого региона не существует!")
        return await dialog_manager.switch_to(TaskCreate.region)

    newTask = TaskDtoBase(
        title=title,
        description=description,
        startline=startline,
        deadline=deadline,
        is_active=is_active,
        status_id=status_id,
        priority_id=priority_id,
        region_id=region_id
    )

    check = await TaskDAO.find_one_or_none(session, newTask)
    if not check:
        await callback.answer("Приступаю к сохранению")
        await TaskDAO.add(session, newTask)
        await callback.answer(f"Задача успешно добавлена!")
        text = "Задача успешно добавлена"
        await callback.message.answer(text, reply_markup=main_admin_kb())

        await dialog_manager.done()
    else:
        await callback.message.answer("Этот задача уже существует!")
        await dialog_manager.back()

    
async def on_update_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")
    
    user_id = callback.from_user.id
    id = dialog_manager.find('id').get_value()
    title = dialog_manager.find('title').get_value()
    description = dialog_manager.find('description').get_value()
    startline = dialog_manager.dialog_data['startline']
    deadline = dialog_manager.dialog_data['deadline']
    is_active = dialog_manager.dialog_data['is_active']

    status_id = dialog_manager.find('status_id').get_value()
    status = await TaskStatusDAO.find_one_or_none_by_id(session, status_id)
    if status is None:
        await callback.message.answer("Такого статуса не существует!")
        return await dialog_manager.switch_to(TaskCreate.status)

    priority_id = dialog_manager.find('priority_id').get_value()
    priority = await TaskPriorityDAO.find_one_or_none_by_id(session, priority_id)
    if priority is None:
        await callback.message.answer("Такого приоритета не существует!")
        return await dialog_manager.switch_to(TaskCreate.priority)

    region_id = dialog_manager.find('region_id').get_value()
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

        await session.commit()

        await callback.answer(f"Запись задачи успешно обновлена!")
        text = "Запись задачи успешно сохранена"
        await callback.message.answer(text, reply_markup=main_admin_kb())

        await dialog_manager.done()
    else:
        await callback.message.answer("Запись задачи не найдена!")
        await dialog_manager.switch_to(TaskUpdate.id)


async def process_delete_task(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

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
            region_id=task.region_id
        )
        count = await TaskDAO.delete(session, taskDto)
        text = f"Удалено {count} записей"
        await session.commit()
        await call.answer(text)
        
        await dialog_manager.done()
    else:
        await call.answer("Запись задачи не найдена!\nВведите другой id.")
