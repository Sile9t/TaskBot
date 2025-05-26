from typing import List
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def user_menu_kb():
    kb = InlineKeyboardBuilder()
    
    kb.button(text="📋 Список пользователей", callback_data="user_list")
    kb.button(text="➕ Добавить пользователя", callback_data="user_add")
    kb.button(text="🖋 Редактировать пользователя", callback_data="user_update")
    kb.button(text="➖ Удалить пользователя", callback_data="user_delete")
    kb.button(text="Назад", callback_data="admin_panel")
    kb.adjust(2, 2, 1)

    return kb.as_markup()
