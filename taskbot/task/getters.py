from loguru import logger
from aiogram_dialog import DialogManager
from taskbot.dao.dao import TaskDAO, TaskStatusDAO, TaskPriorityDAO, RegionDAO

async def get_all_tasks(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    tasks = await TaskDAO.find_all(session)
    
    caption = []
    for task in tasks:
        caption.append({
                "id": str(task.id), 
                "title": task.title,
                "description": task.description,
                "startline": task.startline,
                "deadline": task.deadline,
                "is_active": 'Да' if task.is_active else 'Нет',
                "status": task.status.title,
                "priority": task.priority.title,
                "region": task.region.name if task.region else None,
                'updated_at': task.updated_at,
                'created_at': task.created_at
            })
        
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
    region_id = dialog_manager.dialog_data['region_id']
    region = await RegionDAO.find_one_or_none_by_id(session, region_id)

    confirmed_text = (
        f"<b>Подтверждение добавления задачи</b>\n\n"
        f" Название: {title}\n"
        f" Описание: {description}\n"
        f" Дата начала: {startline}\n"
        f" Дата окончания: {deadline}\n"
        f" Активна: {is_active_text}\n"
        f" Статус: {status.title}\n"
        f" Приоритет: {priority.title}\n"
        f" Регион: {region.name}\n\n"
        "✅ Все ли верно?"
    )

    return {"confirmed_text": confirmed_text}