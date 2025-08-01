from aiogram_dialog import Dialog

from ..region.state import RegionCreate, RegionUpdate, RegionWireChat
from ..region.windows import get_regions_window, get_region_id_window, get_region_name_window, get_region_description_window, get_create_confirmation_window, get_update_confirmation_window, get_delete_window, get_wire_confirmation_window

region_create_dialog = Dialog(
    get_region_name_window(RegionCreate),
    get_region_description_window(RegionCreate),
    get_create_confirmation_window(),
    getter={ "update": False }
)

regions_read_dialog = Dialog(
    get_regions_window(),
)

region_update_dialog = Dialog(
    get_region_id_window(RegionUpdate),
    get_region_name_window(RegionUpdate),
    get_region_description_window(RegionUpdate),
    get_update_confirmation_window(),
    getter={ "update": True }
)

region_delete_dialog = Dialog(
    get_delete_window()
)

region_wire_chat_dialog = Dialog(
    get_region_id_window(RegionWireChat),
    get_wire_confirmation_window()    
)