from aiogram_dialog import Dialog

from ..role.state import RoleCreate, RoleUpdate
from ..role.windows import get_roles_window, get_role_id_window, get_role_name_window, get_role_description_window, get_create_confirmation_window, get_update_confirmation_window, get_delete_window

role_create_dialog = Dialog(
    get_role_name_window(RoleCreate),
    get_role_description_window(RoleCreate),
    get_create_confirmation_window(),
    getter={ 'update': False }
)

roles_read_dialog = Dialog(
    get_roles_window()
)

role_update_dialog = Dialog(
    get_role_id_window(RoleUpdate),
    get_role_name_window(RoleUpdate),
    get_role_description_window(RoleUpdate),
    get_update_confirmation_window(),
    getter={ 'update': True }
)

role_delete_dialog = Dialog(
    get_delete_window()
)