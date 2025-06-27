from aiogram.utils.keyboard import InlineKeyboardBuilder

def task_menu_kb(userRoleId: int = 3):
    kb = InlineKeyboardBuilder()
    
    kb.button(text="📋 Список задач", callback_data="task_list")
    if (userRoleId < 3):
        kb.button(text="➕ Добавить задачу", callback_data="task_add")
        kb.button(text="🖋 Редактировать задачу", callback_data="task_update")
        kb.button(text="➖ Удалить задачу", callback_data="task_delete")
        kb.button(text="Назад", callback_data="admin_panel")
    kb.adjust(2, 2, 1)

    return kb.as_markup()


def task_update_menu(userRoleId: int = 3):
    kb = InlineKeyboardBuilder()

    if (userRoleId < 3):
        kb.button(text="📋 Изменить полностью", callback_data="task_full_update")
        kb.button(text="🗓 Изменить даты", callback_data="task_dates_update")
    kb.button(text="✔ Изменить статус", callback_data="task_status_update")
    if (userRoleId < 3):
        kb.button(text="🔥 Изменить приоритет", callback_data="task_priority_update")
        kb.button(text="🌍 Изменить регион", callback_data="task_region_update")
        kb.button(text="👷 Назначить исполнителей", callback_data="task_set_performers")
    kb.button(text="В меню", callback_data="admin_panel")
    kb.button(text="Назад", callback_data="task_menu")
    kb.adjust(2, 2, 2)

    return kb.as_markup()
