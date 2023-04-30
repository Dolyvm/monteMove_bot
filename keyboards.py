# -*- coding: utf-8 -*-

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

to_manager_button = InlineKeyboardButton(text='У меня остались вопросы, хочу поговорить с сотрудником',
                                         url='t.me/Monte_Manager')

start_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='ВНЖ/Документы', callback_data='residence/docs'),
    InlineKeyboardButton(text='Справка о несудимости', callback_data='criminal_record'),
    InlineKeyboardButton(text='Обмен валют', callback_data='exchange'),
    InlineKeyboardButton(text='Грузоперевозки', callback_data='gruz'),
    InlineKeyboardButton(text='Аренда авто', callback_data='auto'),
    InlineKeyboardButton(text='Трансферы/Визаран', callback_data='transfer'),
    InlineKeyboardButton(text='Недвижимость', callback_data='realty'),
    InlineKeyboardButton(text='Проверенные мастера Черногории', callback_data='masters'),
    InlineKeyboardButton(text='Досуг', callback_data='dosug'),
    InlineKeyboardButton(text='Быт', callback_data='byt'),
    InlineKeyboardButton(text='Связь с нами', url='t.me/Monte_Manager'),
))
back_button = InlineKeyboardButton(text='Назад', callback_data='back')
back_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back')]])


auto_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Арендовать авто', callback_data='rent_auto'),
    InlineKeyboardButton(text='Сдать своё авто в аренду', callback_data='give_rent_auto'),
    back_button
))

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
    InlineKeyboardButton(text='Сдать жилье', callback_data='give_rent'),
    InlineKeyboardButton(text='Продать жилье', callback_data='sell'),
    back_button
))

trans_vis_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Встретить из аэропорта', callback_data='meet_port'),
    InlineKeyboardButton(text='Из города в город', callback_data='from_c_to_c'),
    InlineKeyboardButton(text='Визаран', callback_data='visarun'),
    back_button
))

'''InlineKeyboardButton(text='Нал € за Криптовалюту', callback_data='crypto'),
    InlineKeyboardButton(text='Нал €$₽ МСК - Наличные € чрнг', callback_data='msk_chern'),
    InlineKeyboardButton(text='Нал €$₽ СПБ - Наличные € ЧРНГ', callback_data='spb_chern'),
    InlineKeyboardButton(text='Нал € в ЧРНГ за $€ на РФ Банках', callback_data='rf_bank'),
    InlineKeyboardButton(text='Онлайн сервисы / авиабилеты', callback_data='online_avia'),
    InlineKeyboardButton(text='Другое', callback_data='other'),'''

exchange_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Оставить заявку', callback_data='leave_order'),
    back_button
))

residence_docs_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Получить ВНЖ', callback_data='get_residence'),
    InlineKeyboardButton(text='Другое', callback_data='other'),
    back_button
))

realty_final_kb = ReplyKeyboardMarkup().add(
    KeyboardButton(text='Завершить отправку файлов')
)


residence_options_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='ВНЖ на основании открытия юр.лица', callback_data='yur_face'),
    # InlineKeyboardButton(text='ВНЖ на основании трудоустройства', callback_data='employer'),
    InlineKeyboardButton(text='ВНЖ на основании владения недвижимостью', callback_data='realty_ownership'),
    InlineKeyboardButton(text='Другое', callback_data='other'),
    back_button
))

open_company_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Увидеть список документов', callback_data='show_docs'),
    InlineKeyboardButton(text='Прикрепить документы', callback_data='upload_docs'),
    to_manager_button,
    back_button
))

employer_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Оставить заявку', callback_data='leave_order'),
    to_manager_button,
    back_button
))


beauty_masters_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Бровист Херцег-Нови', callback_data='brovi'),
    InlineKeyboardButton(text='Мастер по ресницам Херцег-Нови', callback_data='resnitsy'),
    back_button
))

masters_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Бьюти сфера', callback_data='beauty'),
    InlineKeyboardButton(text='Работы по дому и стройка', callback_data='byt_uslugi'),
    InlineKeyboardButton(text='Психология', callback_data='psycho'),
    InlineKeyboardButton(text='Фотографы', callback_data='photographer'),
    back_button
))


url_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Ссылка на группу', url='https://t.me/MonteMoveChat '),
    back_button
))


number_request = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
number_button = KeyboardButton('Оставить номер', request_contact=True)
number_request.add(number_button)

yur_kb = InlineKeyboardMarkup(row_width=1).add(*(
    InlineKeyboardButton(text='Прикрепить документы', callback_data='send_docs'),
    to_manager_button,
    back_button
))
