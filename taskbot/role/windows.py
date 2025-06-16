from operator import itemgetter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel, NumberedPager, Row, Next, SwitchTo, CurrentPage, NextPage, PrevPage, FirstPage, LastPage
from aiogram_dialog.widgets.kbd.select import OnItemClick
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.utils import WidgetSrc
from taskbot.role.getters import get_all_roles, get_confirmed_data, get_role_id_tuples
from taskbot.general.handlers import cancel_logic
from taskbot.role.handlers import (
    go_menu, on_role_selected, on_role_delete_selected, on_create_confirmation, on_update_confirmation, process_delete_role, on_role_id_input_error
)
from taskbot.role.state import RoleCreate, RoleRead, RoleUpdate, RoleDelete

MAIN_BTNS = Row(
            Cancel(Const("В меню"), on_click=go_menu),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        )

def get_roles_window(*widgets: WidgetSrc, state: State = RoleRead.id, main_btns: Row = MAIN_BTNS):
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

        Row(
            FirstPage(
                scroll="roles_list", text=Format("⏮️ {target_page1}"),
            ),
            PrevPage(
                scroll="roles_list", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="roles_list", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="roles_list", text=Format("▶️"),
            ),
            LastPage(
                scroll="roles_list", text=Format("{target_page1} ⏭️"),
            ),
        ),

        *widgets,

        main_btns,
        
        getter=get_all_roles,
        state=state,
    )


def get_role_selection_window(*widgets: WidgetSrc, state: State = RoleUpdate.id, on_role_click: OnItemClick[Select[str], str] | WidgetEventProcessor | None = on_role_selected, main_btns: Row = MAIN_BTNS):
    return Window(
        Format("{text_table}"),

        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id='select_role',
                items='role_id_tuples',
                item_id_getter=itemgetter(1),
                on_click=on_role_click
            ),
            width=1,
            height=5,
            hide_pager=True,
            id='scroll_role',
        ),

        Row(
            FirstPage(
                scroll="scroll_role", text=Format("⏮️ {target_page1}"),
            ),
            PrevPage(
                scroll="scroll_role", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="scroll_role", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="scroll_role", text=Format("▶️"),
            ),
            LastPage(
                scroll="scroll_role", text=Format("{target_page1} ⏭️"),
            ),
        ),

        *widgets,

        main_btns,
        
        getter=get_role_id_tuples,
        state=state,
    )


def get_role_id_window(stateGroup: StatesGroup = RoleUpdate):
    return get_role_selection_window(
        Const("Выберите должность для редактирования"),

        state=stateGroup.id,
        on_role_click=on_role_selected,
        main_btns=MAIN_BTNS
    )


def get_role_name_window(stateGroup: StatesGroup = RoleCreate):
    return Window(
        Const("Введите название должности."),
        Format("Текущее значение: <code>{dialog_data[role].name}</code>", when='update'),
        
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
        Format("Текущее значение: <code>{dialog_data[role].description}</code>", when='update'),
        
        TextInput(
            id="description",
            on_success=Next()
        ),

        Group(
            Next(Const("Пропустить")),         
            MAIN_BTNS,
        ),
        state=stateGroup.description,
    )


def get_create_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_create_confirmation),
            MAIN_BTNS,
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
    return get_role_selection_window(
        Const("Выберите должность для удаления"),

        state=RoleDelete.id,
        on_role_click=on_role_delete_selected,
        main_btns=MAIN_BTNS
    )
