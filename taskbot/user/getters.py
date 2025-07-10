from aiogram_dialog import DialogManager

from ..dao.dao import UserDAO, RoleDAO, RegionDAO

async def get_all_users(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    users = await UserDAO.find_all(session)
    
    caption = []
    for user in users:
        caption.append(user.getFullCaption())
        
    return {
        "users": caption, 
        "text_table" : f"Всего найдено {len(users)} пользователей."
    }


async def get_performer_id_tuples(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    
    users = await UserDAO.find_all(session)
    caption = []
    for user in users: 
        caption.append(
            user.getRoleTitleFullNameAndIdTuple()
        )

    return {
        "performer_id_tuples": caption,
        "text_table" : f"Всего найдено {len(users)} пользователей."
    }


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    first_name = dialog_manager.find("first_name").get_value()
    last_name = dialog_manager.find("last_name").get_value()
    role = dialog_manager.dialog_data["role"]
    if (dialog_manager.dialog_data.get("region_id")):
        region_id = dialog_manager.dialog_data.get("region_id")
        region = await RegionDAO.find_one_or_none_by_id(session, region_id)
    
    confirmed_text = (
        f"<b>Подтверждение добавления пользователя</b>\n\n"
        f" Имя: {first_name}\n"
        f" Фамилия: {last_name}\n"
        f" Должность: {role.name}\n"
        f" Регион: {region.name if region else None}\n\n"
        "✅ Все ли верно?"
    )

    return {"confirmed_text": confirmed_text}