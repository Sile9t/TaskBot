from operator import itemgetter
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Cancel, Row, Next, CurrentPage, NextPage, PrevPage, FirstPage, LastPage
from aiogram_dialog.widgets.kbd.select import OnItemClick
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.utils import WidgetSrc

from ..status.getters import get_all_statuses, get_status_id_tuples, get_confirmed_data
from ..general.handlers import cancel_logic
from ..status.handlers import (
    go_menu, on_status_selected, on_create_confirmation, on_update_confirmation, process_delete_status, on_status_id_input_error
)
from ..status.state import StatusCreate, StatusRead, StatusUpdate, StatusDelete


MAIN_BTNS = Row(
            Cancel(Const("В меню"), on_click=go_menu),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        )

def get_statuses_window(*widgets: WidgetSrc, state: State = StatusRead.id):
    return Window(
        Format("{text_table}"),
        
        List(
            Format(
                "Статус №{item[id]}\n"
                    "Название: {item[title]}\n"
                    "Описание: {item[description]}\n"
            ),
            items="statuses",
            id='statuses_list',
            page_size=10
        ),

        Row(
            FirstPage(
                scroll="statuses_list", text=Format("⏮️ {target_page1}"),
            ),
            PrevPage(
                scroll="statuses_list", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="statuses_list", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="statuses_list", text=Format("▶️"),
            ),
            LastPage(
                scroll="statuses_list", text=Format("{target_page1} ⏭️"),
            ),
        ),

        *widgets,

        MAIN_BTNS,
        
        getter=get_all_statuses,
        state=state,
    )


def get_status_selection_window(*widgets: WidgetSrc, state: State = StatusUpdate.id, on_status_click: OnItemClick[Select[str], str] | WidgetEventProcessor | None = on_status_selected, main_btns: Row = MAIN_BTNS):
    return Window(
        Format("{text_table}"),

        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id='select_status',
                items='status_id_tuples',
                item_id_getter=itemgetter(1),
                on_click=on_status_click
            ),
            width=1,
            height=5,
            hide_pager=True,
            id='scroll_status',
        ),

        Row(
            FirstPage(
                scroll="scroll_status", text=Format("⏮️ {target_page1}"),
            ),
            PrevPage(
                scroll="scroll_status", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="scroll_status", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="scroll_status", text=Format("▶️"),
            ),
            LastPage(
                scroll="scroll_status", text=Format("{target_page1} ⏭️"),
            ),
        ),

        *widgets,

        main_btns,
        
        getter=get_status_id_tuples,
        state=state,
    )


def get_status_id_window(stateGroup: StatesGroup = StatusUpdate):
    return get_statuses_window(
        Const("Введите номер записи статуса для изменения."),
        
        TextInput(
            id="id",
            type_factory=int,
            on_error=on_status_id_input_error,
            on_success=Next()
        ),
        state=stateGroup.id
    )


def get_status_title_window(stateGroup: StatesGroup = StatusCreate):
    return Window(
        Const("Введите название статуса."),
        
        TextInput(
            id="title",
            on_success=Next()
        ),

        MAIN_BTNS,
        
        state=stateGroup.title,
    )


def get_status_description_window(stateGroup: StatesGroup = StatusCreate):
    return Window(
        Const("Введите описание статуса."),
        
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

        state=StatusCreate.confirmation,
        getter=get_confirmed_data
    )


def get_update_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_update_confirmation),
            MAIN_BTNS,
        ),

        state=StatusUpdate.confirmation,
        getter=get_confirmed_data
    )


def get_delete_window():
    return get_statuses_window(
        Const("Введите номер записи статуса."),
        TextInput(
            id="id",
            type_factory=int,
            on_success=Next(on_click=process_delete_status)
        ),
        state=StatusDelete.id
    )
