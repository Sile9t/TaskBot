from loguru import logger
from aiogram_dialog import DialogManager
from taskbot.dao.dao import TaskPriorityDAO

async def get_all_priorities(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    priorities = await TaskPriorityDAO.find_all(session)
    
    return {
        "priorities": [priority.to_dict() for priority in priorities], 
        "text_table" : f"Всего найдено {len(priorities)} приоритетов."
    }


async def get_priority_id_tuples(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    priorities = await TaskPriorityDAO.find_all(session)
    
    caption = []
    for priority in priorities:
        caption.append((priority.title, priority.id))

    return {
        "priority_id_tuples": caption, 
        "text_table" : f"Всего найдено {len(priorities)} приоритетов."
    }


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    value = dialog_manager.find("value").get_value()
    title = dialog_manager.find("title").get_value()
    description = dialog_manager.find("description").get_value()

    confirmed_text = (
        f"<b>Подтверждение добавления приоритета</b>\n\n"
        f" Значение: {value}\n"
        f" Название: {title}\n"
        f" Описание: {description}\n\n"
        "✅ Все ли верно?"
    )

    return {"confirmed_text": confirmed_text}