from operator import itemgetter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel, NumberedPager, Row, Next, SwitchTo, FirstPage, LastPage, NextPage, PrevPage, CurrentPage
from aiogram_dialog.widgets.kbd.select import OnItemClick
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.utils import WidgetSrc
from taskbot.region.kbs import region_menu_kb
from taskbot.region.getters import get_all_regions, get_region_id_tuples, get_confirmed_data
from taskbot.region.handlers import (
    go_menu, cancel_logic, on_region_selected, on_create_confirmation, on_update_confirmation, process_delete_region, on_region_id_input_error
)
from taskbot.region.state import RegionCreate, RegionRead, RegionUpdate, RegionDelete

MAIN_BTNS = Row(
            Cancel(Const("В меню"), on_click=go_menu),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        )

def get_regions_window(*widgets: WidgetSrc, state: State = RegionRead.id, main_btns: Row = MAIN_BTNS):
    return Window(
        Format("{text_table}"),
        
        List(
            Format(
                "Регион №{item[id]}\n"
                    "Название: {item[name]}\n"
                    "Описание: {item[description]}\n"
            ),
            items="regions",
            id='regions_list',
            page_size=10
        ),

        Row(
            FirstPage(
                scroll="regions_list", text=Format("⏮️ {target_page1}"),
            ),
            PrevPage(
                scroll="regions_list", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="regions_list", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="regions_list", text=Format("▶️"),
            ),
            LastPage(
                scroll="regions_list", text=Format("{target_page1} ⏭️"),
            ),
        ),

        *widgets,

        main_btns,
        
        getter=get_all_regions,
        state=state,
    )


def get_region_selection_window(*widgets: WidgetSrc, state: State = RegionUpdate.id, on_region_click: OnItemClick[Select[str], str] | WidgetEventProcessor | None = on_region_selected, main_btns: Row = MAIN_BTNS):
    return Window(
        Format("{text_table}"),

        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id='select_region',
                items='region_id_tuples',
                item_id_getter=itemgetter(1),
                on_click=on_region_click
            ),
            width=1,
            height=5,
            hide_pager=True,
            id='scroll_no_pager',
        ),

        Row(
            FirstPage(
                scroll="scroll_no_pager", text=Format("⏮️ {target_page1}"),
            ),
            PrevPage(
                scroll="scroll_no_pager", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="scroll_no_pager", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="scroll_no_pager", text=Format("▶️"),
            ),
            LastPage(
                scroll="scroll_no_pager", text=Format("{target_page1} ⏭️"),
            ),
        ),

        *widgets,

        main_btns,
        
        getter=get_region_id_tuples,
        state=state,
    )


def get_region_id_window(stateGroup: StatesGroup = RegionUpdate, ):
    return get_regions_window(
        Const("Введите номер региона для изменения."),
        
        TextInput(
            id="id",
            type_factory=int,
            on_error=on_region_id_input_error,
            on_success=Next()
        ),
        state=stateGroup.id
    )


def get_region_name_window(stateGroup: StatesGroup = RegionCreate):
    return Window(
        Const("Введите название региона."),
        
        TextInput(
            id="name",
            on_success=Next()
        ),

        MAIN_BTNS,
        
        state=stateGroup.name,
    )


def get_region_description_window(stateGroup: StatesGroup = RegionCreate):
    return Window(
        Const("Введите название региона."),
        
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

        state=RegionCreate.confirmation,
        getter=get_confirmed_data
    )


def get_update_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_update_confirmation),
            MAIN_BTNS,
        ),

        state=RegionUpdate.confirmation,
        getter=get_confirmed_data
    )


def get_delete_window():
    return get_regions_window(
        Const("Введите номер региона."),
        TextInput(
            id="id",
            type_factory=int,
            on_success=Next(on_click=process_delete_region)
        ),
        state=RegionDelete.id
    )
    return Window(
        Format("{text_table}"),
        
        List(
            Format(
                "Регион №{item[id]}\n"
                    "Название: {item[name]}\n"
                    "Описание: {item[description]}\n"
            ),
            items="regions",
            id='regions_list',
            page_size=10
        ),
        NumberedPager(
            scroll='regions_list'
        ),
        
        Const("Введите номер региона."),
        TextInput(
            id="id",
            type_factory=int,
            on_success=Next(on_click=process_delete_region)
        ),

        MAIN_BTNS,

        getter=get_all_regions,
        state=RegionDelete.id,
    )