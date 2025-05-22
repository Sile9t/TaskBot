from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel, NumberedPager, Row, Next, SwitchTo
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.utils import WidgetSrc
from taskbot.role.getters import get_all_roles, get_confirmed_data
from taskbot.role.handlers import (
    cancel_logic, on_role_selected, on_create_confirmation, on_update_confirmation, process_delete_role, on_role_id_input_error
)
from taskbot.role.state import RoleCreate, RoleRead, RoleUpdate, RoleRemove

MAIN_BTNS = Row(
            Back(Const("Назад")),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        )

def get_roles_window(*widgets: WidgetSrc, state: State = RoleRead.id):
    return Window(
        Format("{text_table}"),
        
        List(
            Format(
                "Должность №{item[id]}\n"
                    "Название: {item[name]}\n"
                    "Описание: {item[description]}\n"
            ),
            items="roles",
            id='roles_list',
            page_size=10
        ),

        NumberedPager(
            scroll='roles_list'
        ),

        *widgets,

        MAIN_BTNS,
        
        getter=get_all_roles,
        state=state,
    )


def get_role_id_window(stateGroup: StatesGroup = RoleUpdate, ):
    return get_all_roles(
        Const("Введите номер должности для изменения."),
        
        TextInput(
            id="id",
            type_factory=int,
            on_error=on_role_id_input_error,
            on_success=Next()
        ),
        state=stateGroup.id
    )
    return Window(
        Format("{text_table}"),
        
        List(
            Format(
                "Должность №{item[id]}\n"
                    "Название: {item[name]}\n"
                    "Описание: {item[description]}\n"
            ),
            items="roles",
            id='roles_list',
            page_size=10
        ),

        NumberedPager(
            scroll='roles_list'
        ),

        Const("Введите номер должности для изменения."),
        
        TextInput(
            id="id",
            type_factory=int,
            on_error=on_role_id_input_error,
            on_success=Next()
        ),

        MAIN_BTNS,

        getter=get_all_roles,
        state=stateGroup.id
    )


def get_role_name_window(stateGroup: StatesGroup = RoleCreate):
    return Window(
        Const("Введите название должности."),
        
        TextInput(
            id="name",
            on_success=Next()
        ),

        MAIN_BTNS,
        
        state=stateGroup.name,
    )


def get_role_description_window(stateGroup: StatesGroup = RoleCreate):
    return Window(
        Const("Введите название должности."),
        
        TextInput(
            id="description",
            on_success=Next()
        ),

        Group(
            Next(Const("Пропустить")),         
            Back(Const("Назад")),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        ),
        state=stateGroup.description,
    )


def get_create_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_create_confirmation),
            Back(Const("Назад")),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        ),

        state=RoleCreate.confirmation,
        getter=get_confirmed_data
    )


def get_update_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_update_confirmation),
            MAIN_BTNS,
        ),

        state=RoleUpdate.confirmation,
        getter=get_confirmed_data
    )


def get_delete_window():
    return Window(
        Format("{text_table}"),
        
        List(
            Format(
                "Должность №{item[id]}\n"
                    "Название: {item[name]}\n"
                    "Описание: {item[description]}\n"
            ),
            items="roles",
            id='roles_list',
            page_size=10
        ),
        NumberedPager(
            scroll='roles_list'
        ),
        
        Const("Введите номер должности."),
        TextInput(
            id="id",
            type_factory=int,
            on_success=Next(on_click=process_delete_role)
        ),

        MAIN_BTNS,

        getter=get_all_roles,
        state=RoleRemove.id,
    )