from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Next
from taskbot.role.getters import get_all_roles, get_confirmed_data
from taskbot.role.handlers import (
    cancel_logic, on_role_selected, on_role_name_input, on_role_description_input, on_confirmation
)
from taskbot.role.state import FormCreate

def get_roles_window():
    return Window(
        Format("{text_table}"),
        
        ScrollingGroup(
            Select(
                Format(
                    "Должность №{item[id]}\n" \
                        "Название: {item[name]}\n" \
                        "Описание: {item[description]}"
                ),
                id="role_select",
                item_id_getter=lambda item: str(item["id"]),
                items="roles",
                on_click=on_role_selected,
            ),
            id="roles_scrolling",
            width=2,
            height=3
        ),
        
        Group(
            Back(Const("Назад")),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        ),
        
        getter=get_all_roles,
        state=FormCreate.name,
    )

#TODO: fix role name input getter
def get_role_name_window():
    return Window(
        Const("Введите название должности."),
        
        TextInput(
            id="name",
            on_success=Next()
        ),

        Group(            
            Back(Const("Назад")),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        ),
        state=FormCreate.name,
    )

def get_role_description_window():
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
        state=FormCreate.description,
    )

def get_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_confirmation),
            Back(Const("Назад")),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        ),
        
        state=FormCreate.confirmation,
        getter=get_confirmed_data
    )