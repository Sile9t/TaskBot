from aiogram_dialog import DialogManager
from taskbot.dao.dao import RoleDAO

async def get_all_roles(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    roles = await RoleDAO.find_all(session)
    
    return {
        "roles": [role.to_dict() for role in roles], 
        "text_table" : f"Всего найдено {len(roles)} должностей."
    }


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    name = dialog_manager.find("name").get_value()
    description = dialog_manager.find("description").get_value()

    confirmed_text = (
        f"<b>Подтверждение добавления должности</b>\n\n"
        f" Название: {name}\n"
        f" Описание: {description}\n\n"
        "✅ Все ли верно?"
    )

    return {"confirmed_text": confirmed_text}