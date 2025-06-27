from aiogram_dialog import DialogManager

from ..dao.dao import TaskDAO, TaskStatusDAO, TaskPriorityDAO

async def get_all_tasks(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    tasks = await TaskDAO.find_all(session)
    
    caption = []
    for task in tasks:
        caption.append(task.getFullCaption())
        
    return {
        "tasks": caption, 
        "text_table" : f"Всего найдено {len(tasks)} задач."
    }


async def get_is_active_variants(dialog_manager: DialogManager, **kwargs):

    caption = [
        ('Да', True),
        ('Нет', False)
    ]

    return {
        "is_active_variants" : caption
    }


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")

    title = dialog_manager.find('title').get_value()
    description = dialog_manager.find('description').get_value()
    startline = dialog_manager.dialog_data['startline']
    deadline = dialog_manager.dialog_data['deadline']
    is_active = dialog_manager.dialog_data['is_active']
    is_active_text = 'Да' if is_active else 'Нет'
    status_id = dialog_manager.dialog_data['status_id']
    status = await TaskStatusDAO.find_one_or_none_by_id(session, status_id)
    priority_id = dialog_manager.dialog_data['priority_id']
    priority = await TaskPriorityDAO.find_one_or_none_by_id(session, priority_id)
    region = dialog_manager.dialog_data['region']

    confirmed_text = (
        f"<b>Подтверждение добавления задачи</b>\n\n"
        f" Название: {title}\n"
        f" Описание: {description}\n"
        f" Дата начала: {startline.strftime('%d.%m.%Y')}\n"
        f" Дата окончания: {deadline.strftime('%d.%m.%Y')}\n"
        f" Активна: {is_active_text}\n"
        f" Статус: {status.title}\n"
        f" Приоритет: {priority.title}\n"
        f" Регион: {region.name}\n\n"
        "✅ Все ли верно?"
    )

    return {"confirmed_text": confirmed_text}

async def get_changed_dates_data(dialog_manager: DialogManager, **kwargs):
    startline = dialog_manager.dialog_data['startline']
    deadline = dialog_manager.dialog_data['deadline']

    confirmed_text = (
        f"<b>Подтвердите изменение дат</b>\n\n"
        f" Дата начала: {startline.strftime('%d.%m.%Y')}\n"
        f" Дата окончания: {deadline.strftime('%d.%m.%Y')}\n"
        "✅ Все ли верно?"
    )

    return {"confirmed_text": confirmed_text}
