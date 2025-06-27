from aiogram_dialog import DialogManager

from ..dao.dao import RoleDAO

async def get_all_roles(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    roles = await RoleDAO.find_all(session)
    
    return {
        "roles": [role.to_dict() for role in roles], 
        "text_table" : f"Всего найдено {len(roles)} должностей."
    }

async def get_role_id_tuples(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    roles = await RoleDAO.find_all(session)
    
    caption = []
    for role in roles:
        caption.append((role.name, role.id))

    return {
        "role_id_tuples": caption, 
        "text_table" : f"Всего найдено {len(roles)} регионов."
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