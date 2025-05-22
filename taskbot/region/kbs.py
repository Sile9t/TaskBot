from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def region_menu_kb():
    kb = InlineKeyboardBuilder()
    
    kb.button(text="📋 Список регионов", callback_data="region_list")
    kb.button(text="➕ Добавить регион", callback_data="region_create")
    kb.button(text="🖋 Редактировать регион", callback_data="region_update")
    kb.button(text="➖ Удалить регион", callback_data="region_delete")
    kb.button(text="Назад", callback_data="admin_panel")
    kb.adjust(2, 2, 1)

    return kb.as_markup()