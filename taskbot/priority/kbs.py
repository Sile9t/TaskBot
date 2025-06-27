from aiogram.utils.keyboard import InlineKeyboardBuilder

def priority_menu_kb():
    kb = InlineKeyboardBuilder()
    
    kb.button(text="📋 Список приоритетов", callback_data="priority_list")
    kb.button(text="➕ Добавить приоритет", callback_data="priority_add")
    kb.button(text="🖋 Редактировать приоритет", callback_data="priority_update")
    kb.button(text="➖ Удалить приоритет", callback_data="priority_delete")
    kb.button(text="Назад", callback_data="admin_panel")
    kb.adjust(2, 2, 1)

    return kb.as_markup()
