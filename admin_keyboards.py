from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_admin_kb = InlineKeyboardMarkup(row_width=1).add(*[
    InlineKeyboardButton('Добавить новую вкладку', callback_data="add_new_tab"),
    InlineKeyboardButton('Изменить существующее', callback_data="edit_existing"),
])

sphere_options_kb = InlineKeyboardMarkup(row_width=1).add(*[
    InlineKeyboardButton('Открыть эту вкладку', callback_data="open_tab"),
    InlineKeyboardButton('Изменить название', callback_data="edit_name"),
    InlineKeyboardButton('Добавить мастера', callback_data="add_master"),
    InlineKeyboardButton('Удалить вкладку', callback_data="remove_tab"),
])

master_options_kb = InlineKeyboardMarkup(row_width=1).add(*[
    InlineKeyboardButton('Изменить название', callback_data="edit_name"),
    InlineKeyboardButton('Изменить внутренний текст', callback_data="edit_text"),
    InlineKeyboardButton('Удалить мастера', callback_data="remove_master"),
])

ap_start_kb = InlineKeyboardMarkup(row_width=1).add(*[
    InlineKeyboardButton("Добавить новую вкладку", callback_data="add_tab"),
    InlineKeyboardButton("Добавить нового мастера", callback_data="add_master"),
    InlineKeyboardButton("Изменить инфу о мастере", callback_data="edit_master"),
    InlineKeyboardButton("Удалить мастера", callback_data="remove_master"),
    InlineKeyboardButton("Изменить название вкладки", callback_data="edit_tab"),
    InlineKeyboardButton("Удалить вкладку", callback_data="remove_tab")
])
