from aiogram_dialog import DialogManager
from taskbot.dao.dao import TaskDAO

async def get_tasks(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    tasks = await TaskDAO.find_all(session)
    
    return {
        "tasks": [task.to_dict() for task in tasks], 
        "text_table" : f"Всего найдено {len(tasks)} должностей."
    }