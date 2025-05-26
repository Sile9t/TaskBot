from aiogram_dialog import Dialog
from taskbot.user.state import UserCreate, UserUpdate
from taskbot.user.windows import get_users_window, get_user_id_window, get_user_first_name_window, get_user_last_name_window, get_user_region_window, get_user_role_window, get_create_confirmation_window, get_update_confirmation_window, get_delete_window

user_create_dialog = Dialog(
    get_user_first_name_window(UserCreate),
    get_user_last_name_window(UserCreate),
    get_user_role_window(UserCreate),
    get_user_region_window(UserCreate),
    get_create_confirmation_window()
)

users_read_dialog = Dialog(
    get_users_window()
)

user_update_dialog = Dialog(
    get_user_id_window(UserUpdate),
    get_user_first_name_window(UserUpdate),
    get_user_last_name_window(UserUpdate),
    get_user_role_window(UserUpdate),
    get_user_region_window(UserUpdate),
    get_update_confirmation_window()
)

user_delete_dialog = Dialog(
    get_delete_window()
)