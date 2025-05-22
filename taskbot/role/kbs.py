from typing import List
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def role_menu_kb():
    kb = InlineKeyboardBuilder()
    
    kb.button(text="📋 Список должностей", callback_data="role_list")
    kb.button(text="➕ Добавить должность", callback_data="role_add")
    kb.button(text="🖋 Редактировать должность", callback_data="role_update")
    kb.button(text="➖ Удалить должность", callback_data="role_delete")
    kb.button(text="Назад", callback_data="admin_panel")
    kb.adjust(2, 2, 1)

    return kb.as_markup()
