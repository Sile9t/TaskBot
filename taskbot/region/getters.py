from aiogram_dialog import DialogManager
from taskbot.dao.dao import RegionDAO

async def get_all_regions(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    regions = await RegionDAO.find_all(session)
    
    return {
        "regions": [region.to_dict() for region in regions], 
        "text_table" : f"Всего найдено {len(regions)} должностей."
    }


async def get_region_id_tuples(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    regions = await RegionDAO.find_all(session)
    
    caption = []
    for region in regions:
        caption.append((region.name, region.id))

    return {
        "region_id_tuples": caption, 
        "text_table" : f"Всего найдено {len(regions)} регионов."
    }

async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    name = dialog_manager.find("name").get_value()
    description = dialog_manager.find("description").get_value()

    confirmed_text = (
        f"<b>Подтверждение добавления записи</b>\n\n"
        f" Название: {name}\n"
        f" Описание: {description}\n\n"
        "✅ Все ли верно?"
    )

    return {"confirmed_text": confirmed_text}