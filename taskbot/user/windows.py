from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel, NumberedPager, Row, Next, SwitchTo, CurrentPage, NextPage, PrevPage, FirstPage, LastPage
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.utils import WidgetSrc
from taskbot.user.getters import get_all_users, get_confirmed_data
from taskbot.role.windows import get_roles_window
from taskbot.region.windows import get_regions_window
from taskbot.user.handlers import (
    go_menu, cancel_logic, on_user_selected, on_create_confirmation, on_update_confirmation, process_delete_user, on_user_id_input_error
)
from taskbot.user.state import UserCreate, UserRead, UserUpdate, UserDelete

MAIN_BTNS = Row(
            Cancel(Const("В меню"), on_click=go_menu),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        )

def get_users_window(*widgets: WidgetSrc, state: State = UserRead.id):
    return Window(
        Format("{text_table}"),
        
        List(
            Format(
                "ID: {item[id]}\n"
                    "Имя: {item[first_name]}\n"
                    "Фамилия: {item[last_name]}\n"
                    "Должность: {item[role]}\n"
                    "Регион: {item[region]}\n"
            ),
            items="users",
            id='users_list',
            page_size=10
        ),

        Row(
            FirstPage(
                scroll="users_list", text=Format("⏮️ {target_page1}"),
            ),
            PrevPage(
                scroll="users_list", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="users_list", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="users_list", text=Format("▶️"),
            ),
            LastPage(
                scroll="users_list", text=Format("{target_page1} ⏭️"),
            ),
        ),

        *widgets,

        MAIN_BTNS,
        
        getter=get_all_users,
        state=state,
    )


def get_user_id_window(stateGroup: StatesGroup = UserUpdate):
    return get_users_window(
        Const("Введите номер должности для изменения."),
        
        TextInput(
            id="id",
            type_factory=int,
            on_error=on_user_id_input_error,
            on_success=Next()
        ),
        state=stateGroup.id
    )


def get_user_first_name_window(stateGroup: StatesGroup = UserCreate):
    return Window(
        Const("Введите имя пользователя."),
        
        TextInput(
            id="first_name",
            on_success=Next()
        ),

        MAIN_BTNS,
        
        state=stateGroup.first_name,
    )


def get_user_last_name_window(stateGroup: StatesGroup = UserCreate):
    return Window(
        Const("Введите фамилию пользователя."),
        
        TextInput(
            id="last_name",
            on_success=Next()
        ),

        MAIN_BTNS,
        
        state=stateGroup.last_name,
    )


def get_user_role_window(stateGroup: StatesGroup = UserCreate):
    return get_roles_window(
        Const("Введите номер должности."),
        
        TextInput(
            id="role_id",
            on_success=Next()
        ),
        
        state=stateGroup.role
    )
    return Window(
        Const("Введите название должности."),
        
        TextInput(
            id="",
            on_success=Next()
        ),

        Group(
            Next(Const("Пропустить")),         
            MAIN_BTNS,
        ),
        state=stateGroup.region,
    )


def get_user_region_window(stateGroup: StatesGroup = UserCreate):
    return get_regions_window(
        Const("Введите номер региона."),
        
        TextInput(
            id="region_id",
            on_success=Next()
        ),
        Next(Const("Пропустить")),         
        
        state=stateGroup.region
    )
    return Window(
        Const("Введите название должности."),
        
        TextInput(
            id="",
            on_success=Next()
        ),

        Group(
            Next(Const("Пропустить")),         
            MAIN_BTNS,
        ),
        state=stateGroup.region,
    )


def get_create_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_create_confirmation),
            MAIN_BTNS,
        ),

        state=UserCreate.confirmation,
        getter=get_confirmed_data
    )


def get_update_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_update_confirmation),
            MAIN_BTNS,
        ),

        state=UserUpdate.confirmation,
        getter=get_confirmed_data
    )


def get_delete_window():
    return get_users_window(
        Const("Введите номер должности."),
        TextInput(
            id="id",
            type_factory=int,
            on_success=Next(on_click=process_delete_user)
        ),
        state=UserDelete.id
    )
