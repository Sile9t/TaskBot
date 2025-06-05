from loguru import logger
from aiogram_dialog import DialogManager
from taskbot.dao.dao import UserDAO, RoleDAO, RegionDAO

async def get_all_users(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    users = await UserDAO.find_all(session)
    
    caption = []
    for user in users:
        caption.append({
                "id": str(user.id), 
                "telegram_id": user.telegram_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role.name,
                "region": user.region.name if user.region else None,
                'updated_at': user.updated_at,
                'created_at': user.created_at
            })
        
    return {
        "users": caption, 
        "text_table" : f"Всего найдено {len(users)} пользователей."
    }


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    first_name = dialog_manager.find("first_name").get_value()
    last_name = dialog_manager.find("last_name").get_value()
    role_id = dialog_manager.dialog_data["role_id"]
    role = await RoleDAO.find_one_or_none_by_id(session, role_id)
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