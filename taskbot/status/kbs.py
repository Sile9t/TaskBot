from typing import List
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def status_menu_kb():
    kb = InlineKeyboardBuilder()
    
    kb.button(text="📋 Список статусов", callback_data="status_list")
    kb.button(text="➕ Добавить статус", callback_data="status_add")
    kb.button(text="🖋 Редактировать статус", callback_data="status_update")
    kb.button(text="➖ Удалить статус", callback_data="status_delete")
    kb.button(text="Назад", callback_data="admin_panel")
    kb.adjust(2, 2, 1)

    return kb.as_markup()
