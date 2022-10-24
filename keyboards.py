from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_kb = InlineKeyboardMarkup().add(*(
    InlineKeyboardButton(text='Обмен валют', callback_data='exchange'),
    InlineKeyboardButton(text='ВНЖ/Документы', callback_data='residence/docs'),
    InlineKeyboardButton(text='Аренда авто', callback_data='rent_avt'),
    InlineKeyboardButton(text='Трансферы/Визаран', callback_data='transfer'),
    InlineKeyboardButton(text='Грузоперевозки', callback_data='gruz'),
    InlineKeyboardButton(text='Недвижимость', callback_data='realty')
))

back_button = InlineKeyboardButton(text='Назад', callback_data='back')

gruz_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Отправить груз в РФ', callback_data='gruz_rf'),
    InlineKeyboardButton(text='Доставить груз из РФ', callback_data='from_rf'),
    InlineKeyboardButton(text='Перевести груз внутри страны', callback_data='internal'),
    InlineKeyboardButton(text='Другие страны/Другой запрос', callback_data='other_con'),
    back_button
))

realty_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Аренда жилья', callback_data='rent'),
    InlineKeyboardButton(text='Покупка жилья', callback_data='buy'),
    InlineKeyboardButton(text='Сдать жилье', callback_data='hand_over'),
    InlineKeyboardButton(text='Прождать жилье', callback_data='sell_realty'),
    back_button
))

trans_vis_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Встретить из аэропорта', callback_data='meet_port'),
    InlineKeyboardButton(text='Из города в город', callback_data='from_c_to_c'),
    InlineKeyboardButton(text='Визаран', callback_data='visarun'),
    back_button
))


exchange_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='ЕвроНал за безнал рубли', callback_data='eurorub'),
    InlineKeyboardButton(text='ЕвроНал за криптовалюту', callback_data='crypto'),
    InlineKeyboardButton(text='ЕвроНал Мск - ЕвроНал ЧГ', callback_data='msk_chern'),
    InlineKeyboardButton(text='ЕвроНал ЧГ за $/ € на РФ Банках', callback_data='rf_bank'),
    InlineKeyboardButton(text='Оплата он-лайн серивсов / покупка авиабилетов', callback_data='online_avia'),
    InlineKeyboardButton(text='Другое', callback_data='other'),
    back_button
))

residence_docs_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Получить ВНЖ', callback_data='get_residence'),
    InlineKeyboardButton(text='Справка о несудимости', callback_data='criminal_record'),
    InlineKeyboardButton(text='Другое', callback_data='other'),
    back_button
))
