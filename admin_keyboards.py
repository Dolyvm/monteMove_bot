from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# start_admin_kb = InlineKeyboardMarkup(row_width=1).add(*[
#     InlineKeyboardButton('Добавить новую вкладку', callback_data="add_new_tab"),
#     InlineKeyboardButton('Изменить существующее', callback_data="edit_existing"),
# ])

ap_start_kb = InlineKeyboardMarkup(row_width=1).add(*[
    InlineKeyboardButton("Настройка мастеров", callback_data="master"),
    InlineKeyboardButton("Настройка досуга", callback_data="dosug"),
    InlineKeyboardButton("Посмотреть статистику за месяц", callback_data="check_stats")
])

ap_settings_kb = InlineKeyboardMarkup(row_width=1).add(*[
    InlineKeyboardButton("Добавить новую вкладку", callback_data="add_tab"),
    InlineKeyboardButton("Добавить новое поле во вкладку", callback_data="add_field"),
    InlineKeyboardButton("Изменить инфу о поле", callback_data="edit_field"),
    InlineKeyboardButton("Удалить поле", callback_data="remove_field"),
    InlineKeyboardButton("Изменить название вкладки", callback_data="edit_tab"),
    InlineKeyboardButton("Удалить вкладку", callback_data="remove_tab"),
])

sphere_options_kb = InlineKeyboardMarkup(row_width=1).add(*[
    InlineKeyboardButton('Открыть эту вкладку', callback_data="open_tab"),
    InlineKeyboardButton('Изменить название', callback_data="edit_name"),
    InlineKeyboardButton('Добавить мастера', callback_data="add_master"),
    InlineKeyboardButton('Удалить вкладку', callback_data="remove_tab"),
])
