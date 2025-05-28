from loguru import logger
from aiogram_dialog import DialogManager
from taskbot.dao.dao import TaskStatusDAO

async def get_all_statuses(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    statuses = await TaskStatusDAO.find_all(session)
    
    return {
        "statuses": [status.to_dict() for status in statuses], 
        "text_table" : f"Всего найдено {len(statuses)} статусов."
    }


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    title = dialog_manager.find("title").get_value()
    description = dialog_manager.find("description").get_value()

    confirmed_text = (
        f"<b>Подтверждение добавления должности</b>\n\n"
        f" Название: {title}\n"
        f" Описание: {description}\n\n"
        "✅ Все ли верно?"
    )

    return {"confirmed_text": confirmed_text}