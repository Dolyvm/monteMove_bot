from contextlib import suppress

import aiogram
from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, MediaGroup, ReplyKeyboardRemove, \
    InlineKeyboardButton, Contact
from aiogram.utils.exceptions import ValidationError

from functions import get_masters, kb_from_dict
from table_ctrl import generateOrder
from keyboards import start_kb, exchange_kb, residence_docs_kb, back_button, gruz_kb, realty_kb, trans_vis_kb, \
    realty_final_kb, residence_options_kb, open_company_kb, employer_kb, masters_kb, url_kb, auto_kb, number_request, \
    beauty_masters_kb, back_kb
from table_ctrl import update_table
from utils import start_text, option_text, exchange_text, final_text, exchange_order_text, residence_docs_text, \
    gruz_text, realty_text_1, realty_text_2, trans_vis_text_1, trans_vis_text_2, trans_vis_text_3, realty_text_3, \
    realty_text_4, buttons_name_dict, vnj_text, employer_text, vnj_docs_text, zaglushka_text, byt_text, \
    rent_auto_first_text, rent_auto_second_text, rent_auto_third_text, number_text, beauty_text, other_text, \
    vremennie_trudnosti


class UserStates(StatesGroup):
    get_main_number_state = State()
    start_state = State()
    exchange_state = State()
    residence_state = State()
    rent_state = State()
    transfer_state = State()
    gruz_state = State()
    auto_state = State()
    rent_auto_text_state = State()
    second_rent_auto_text_state = State()
    realty_state = State()
    final_state = State()
    realty_final_state = State()
    vnj_state = State()
    vnj_middle_state = State()
    vnj_final_state = State()
    get_documents_state = State()
    master_state = State()
    assistance_state = State()
    beauty_masters_state = State()
    show_master_state = State()


def register_user_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start', 'help'], state='*')
    async def start(message: Message, state: FSMContext):
        await message.answer(start_text.format(message.chat.full_name), reply_markup=start_kb)
        await state.update_data(text=[])
        await UserStates.start_state.set()

    @dp.callback_query_handler(state=UserStates.start_state)
    async def start_options(callback: CallbackQuery, state: FSMContext):
        if callback.data == 'exchange':
            await callback.message.edit_text(option_text, reply_markup=exchange_kb)
            await UserStates.exchange_state.set()
            await state.update_data(category='Обмен Валют')
        elif callback.data == 'residence/docs':
                await callback.message.edit_text(option_text, reply_markup=residence_docs_kb)
                await UserStates.residence_state.set()
                await state.update_data(category='ВНЖ/Документы')
        elif callback.data == 'auto':
                await callback.message.edit_text(text='Аренда авто', reply_markup=auto_kb)
                await UserStates.auto_state.set()
                await state.update_data(category='Авто')

        elif callback.data == 'transfer':
                await callback.message.edit_text(option_text, reply_markup=trans_vis_kb)
                await UserStates.transfer_state.set()
                await state.update_data(category='Трансферы/Визаран')
        elif callback.data == 'gruz':
                await callback.message.edit_text(option_text, reply_markup=gruz_kb)
                await UserStates.gruz_state.set()
                await state.update_data(category='Грузоперевозки')
        elif callback.data == 'realty':
                await callback.message.edit_text(option_text, reply_markup=realty_kb)
                await UserStates.realty_state.set()
                await state.update_data(category='Недвижимость')

        elif callback.data == 'masters':
                await callback.message.edit_text(option_text, reply_markup=kb_from_dict(get_masters()))
                await UserStates.master_state.set()
                await state.update_data(category='Мастера')
        elif callback.data == 'byt':
                await callback.message.edit_text(byt_text, reply_markup=url_kb)
                await UserStates.master_state.set()
                await state.update_data(category='Быт')
        elif callback.data == 'back':
                await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                                 reply_markup=start_kb)

    @dp.callback_query_handler(state=UserStates.exchange_state)
    async def exchange_options(callback: CallbackQuery, state: FSMContext):
        if callback.data == "back":
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                                 reply_markup=start_kb)
            await UserStates.start_state.set()
        elif callback.data == 'other':
            await state.update_data(option=buttons_name_dict[callback.data])
            await callback.message.edit_text(other_text)
            await UserStates.final_state.set()

        else:
            await state.update_data(option=buttons_name_dict[callback.data])
            await callback.message.edit_text(exchange_text)
            await UserStates.final_state.set()

    @dp.callback_query_handler(state=UserStates.auto_state)
    async def auto_options(callback: CallbackQuery, state: FSMContext):
        if callback.data == 'rent_auto':
            await callback.message.edit_text(text=rent_auto_first_text)
            await UserStates.rent_auto_text_state.set()
            await state.update_data(option=buttons_name_dict[callback.data])
       elif callback.data == 'give_rent_auto':
            await callback.message.edit_text(text=rent_auto_third_text)
            await UserStates.final_state.set()
            await state.update_data(option=buttons_name_dict[callback.data])

        elif callback.data == 'back':
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await UserStates.start_state.set()

    @dp.message_handler(state=UserStates.rent_auto_text_state, content_types=['text'])
    async def rent_first_text(message: Message, state: FSMContext):
        await state.update_data(text=message.text)
        await message.answer(text=rent_auto_second_text)
        await UserStates.second_rent_auto_text_state.set()

    @dp.message_handler(state=UserStates.second_rent_auto_text_state, content_types=['text'])
    async def rent_final_text(message: Message, state: FSMContext):
        data = await state.get_data()
        order = generateOrder()
        await state.update_data(order=order)
        await message.answer(text=final_text.format(order))
        await message.bot.send_message(chat_id=-1001591695557,
                                       text=exchange_order_text.format(order, 'тачка',
                                                                       data['text'] + '\n\n' + message.text))
        await message.answer(text=number_text, reply_markup=number_request, parse_mode='Markdown')
        await UserStates.get_main_number_state.set()

    @dp.callback_query_handler(state=UserStates.master_state)
    async def masters_options(callback: CallbackQuery, state: FSMContext):
        masters = get_masters()
        if callback.data == "back":
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await UserStates.start_state.set()
        else:
            kb = kb_from_dict(masters[callback.data])
            if kb:
                await callback.message.edit_text(text='Список мастеров:',
                                                 reply_markup=kb)
                await UserStates.show_master_state.set()
                await state.update_data(master_sphere=callback.data)
            else:
                await callback.message.edit_text(text=zaglushka_text,
                                                 reply_markup=back_kb)

    @dp.callback_query_handler(state=UserStates.show_master_state)
    async def show_master(callback: CallbackQuery, state: FSMContext):
        masters = get_masters()
        data = await state.get_data()
        if callback.data == "back":
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await UserStates.start_state.set()
        else:
            await callback.message.edit_text(text=masters[data['master_sphere']][callback.data],
                                                 reply_markup=back_kb)

    @dp.callback_query_handler(state=UserStates.transfer_state)
    async def transfer_options(callback: CallbackQuery, state: FSMContext):
        if callback.data == "back":
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await UserStates.start_state.set()
        if callback.data ==  'meet_port':
            await callback.message.edit_text(trans_vis_text_1)
            await UserStates.final_state.set()
            await state.update_data(option=buttons_name_dict[callback.data])

        if callback.data == 'from_c_to_c':
            await callback.message.edit_text(trans_vis_text_2)
            await UserStates.final_state.set()
            await state.update_data(option=buttons_name_dict[callback.data])

        if callback.data == 'visarun':
            await callback.message.edit_text(trans_vis_text_3)
            await UserStates.final_state.set()
            await state.update_data(option=buttons_name_dict[callback.data])

    @dp.callback_query_handler(state=UserStates.realty_state)
    async def realty_options(callback: CallbackQuery, state: FSMContext):
        if callback.data == "back":
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await UserStates.start_state.set()
            return
        elif callback.data == 'rent':
            await callback.message.edit_text(realty_text_1)
            await UserStates.final_state.set()

        elif callback.data == 'buy':
            await callback.message.edit_text(realty_text_2)
            await UserStates.final_state.set()

        elif callback.data == 'give_rent':
            await callback.message.answer(realty_text_3, reply_markup=realty_final_kb)
            await UserStates.realty_final_state.set()

        elif callback.data == 'sell':
            await callback.message.answer(realty_text_4, reply_markup=realty_final_kb)
            await UserStates.realty_final_state.set()
        await state.update_data(option=buttons_name_dict[callback.data])

    @dp.callback_query_handler(state=UserStates.residence_state)
    async def residence_options(callback: CallbackQuery, state: FSMContext):
        if callback.data == "back":
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await UserStates.start_state.set()
        if callback.data == 'get_residence':
            await callback.message.edit_text(text=option_text, reply_markup=residence_options_kb)
            await UserStates.vnj_state.set()

        else:
            await callback.message.answer(text=residence_docs_text)
            await UserStates.final_state.set()
            await state.update_data(option=buttons_name_dict[callback.data])

    @dp.callback_query_handler(state=UserStates.gruz_state)
    async def gruz_options(callback: CallbackQuery, state: FSMContext):
        if callback.data == 'back':
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await UserStates.start_state.set()
        else:
            await callback.message.answer(text=gruz_text)
            await UserStates.final_state.set()
            await state.update_data(option=buttons_name_dict[callback.data])

    @dp.callback_query_handler(state=UserStates.vnj_state)
    async def vnj_options(callback: CallbackQuery, state: FSMContext):
        if callback.data == 'open_company':
            await callback.message.edit_text(text=vnj_text, reply_markup=open_company_kb)
            await UserStates.vnj_middle_state.set()
        elif callback.data == 'realty_ownership':
            await callback.message.answer(text=vremennie_trudnosti)
            await UserStates.final_state.set()
        elif callback.data == 'employer':
            await callback.message.edit_text(text=employer_text, reply_markup=employer_kb)
            await UserStates.vnj_middle_state.set()
        elif callback.data == 'other':
            await callback.message.answer(text='Контакты менеджера: ... \nДля перехода в начало введите /start')
            await UserStates.start_state.set()
        elif callback.data == 'back':
            await callback.message.edit_text(text=option_text, reply_markup=residence_docs_kb)
            await UserStates.residence_state.set()
            return
        await state.update_data(option=buttons_name_dict[callback.data])

    @dp.callback_query_handler(state=UserStates.vnj_middle_state)
    async def vnj_middle(callback: CallbackQuery, state: FSMContext):
        if callback.data == 'show_docs':
            await callback.message.edit_text(
                text=vnj_docs_text,
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Назад', callback_data='back2')))

        elif callback.data == 'ask_questions':
            await callback.message.answer(text='Контакты менеджера: ... \nДля перехода в начало введите /start')
            await UserStates.start_state.set()
        elif callback.data == 'upload_docs':
            await callback.message.answer(text=vnj_docs_text, reply_markup=realty_final_kb)
            await UserStates.get_documents_state.set()
        elif callback.data == 'back':
            await callback.message.edit_text(text=option_text, reply_markup=residence_options_kb)
            await UserStates.vnj_state.set()
            return
        elif callback.data == 'back2':
            await callback.message.answer(text=vnj_text, reply_markup=open_company_kb)
        elif callback.data in ('yes', 'no'):
            await callback.message.answer(text=zaglushka_text)
            await UserStates.start_state.set()
            await callback.message.answer(start_text.format(callback.message.chat.full_name), reply_markup=start_kb)

    @dp.message_handler(state=UserStates.get_documents_state, content_types=('photo', 'document', 'text'))
    async def get_documents(message: Message, state: FSMContext):
        if message.text == 'Завершить отправку файлов':
            order = generateOrder()
            await state.update_data(order=order)
            data = await state.get_data()
            if not data.get('text', None):
                await message.answer(text='Отправьте требуемый текст')
                return
            if not data.get('photos', None):
                await message.answer(text='Добавьте требуемые документы')
                return
            media_photo = MediaGroup()
            media_documents = MediaGroup()
            for i in data.get('photos', []):
                media_photo.attach_photo(i)
            for i in data.get('documents', []):
                media_documents.attach_document(i)
            await message.bot.send_message(chat_id=-1001591695557,
                                           text=exchange_order_text.format(
                                               order, data['option'], "\n".join(data['text'])))
            with suppress(ValidationError):
                await message.bot.send_media_group(chat_id=-1001591695557, media=media_photo)
                await message.bot.send_media_group(chat_id=-1001591695557, media=media_documents)
            await message.answer(text=final_text.format(order), reply_markup=ReplyKeyboardRemove())
            await state.update_data(photos=[])
            await state.update_data(documents=[])
            await message.answer(text=number_text, reply_markup=number_request, parse_mode='Markdown')
            await UserStates.get_main_number_state.set()
        elif message.text:
            data = await state.get_data()
            text: list = data.get('text', [])
            text.append(message.text)
            await state.update_data(text=text)
        elif message.photo:
            data = await state.get_data()
            photos: list = data.get('photos', [])
            photos.append(message.photo[-1].file_id)
            await state.update_data(photos=photos)
        elif message.document:
            data = await state.get_data()
            documents: list = data.get('documents', [])
            documents.append(message.document.file_id)
            await state.update_data(documents=documents)

    @dp.message_handler(state=UserStates.final_state, content_types=('photo', 'text'))
    async def get_final(message: Message, state: FSMContext):
        order = generateOrder()
        await state.update_data(order=order)
        await state.update_data(text=message.text)
        data = await state.get_data()
        await message.answer(text=final_text.format(order))
        await message.bot.send_message(chat_id=-1001591695557,
                                       text=exchange_order_text.format(order, data['option'], message.text))
        await UserStates.get_main_number_state.set()
        await message.answer(text=number_text, reply_markup=number_request, parse_mode='Markdown')

    @dp.message_handler(state=UserStates.realty_final_state, content_types=('photo', 'text'))
    async def get_realty_files(message: Message, state: FSMContext):
        if message.text == 'Завершить отправку файлов':
            order = generateOrder()
            await state.update_data(order=order)
            data = await state.get_data()
            if not data.get('text', None):
                await message.answer(text='Добавьте описание фотографий')
                return
            if not data.get('photos', None):
                await message.answer(text='Добавьте фотографии квартиры')
                return
            media = MediaGroup()
            for i in data['photos']:
                media.attach_photo(i)
            await message.bot.send_message(chat_id=-1001591695557,
                                           text=exchange_order_text.format(order, data['option'],
                                                                           '\n'.join(data['text'])))
            await message.bot.send_media_group(chat_id=-1001591695557, media=media)
            await message.answer(text=final_text.format(order), reply_markup=ReplyKeyboardRemove())
            await state.update_data(photos=[])
            await state.update_data(text=[])

            await message.answer(text=number_text, reply_markup=number_request, parse_mode='Markdown')
            await UserStates.get_main_number_state.set()
        elif message.text:
            data = await state.get_data()
            text: list = data.get('text', [])
            text.append(message.text)
            await state.update_data(text=text)
        elif message.photo:
            data = await state.get_data()
            photos: list = data.get('photos', [])
            photos.append(message.photo[-1].file_id)
            await state.update_data(photos=photos)

    @dp.message_handler(content_types=['contact'], state=UserStates.get_main_number_state)
    async def getContactMain(number: Contact, state: FSMContext):
        data = await state.get_data()
        await number.bot.send_message(chat_id=number["from"]["id"],
                                      text="⏳",
                                      reply_markup=ReplyKeyboardRemove())
        await state.update_data(number=number["contact"]["phone_number"])
        await state.update_data(text=[])
        await UserStates.start_state.set()
        await number.bot.send_message(
            chat_id=number["from"]["id"],
            text=start_text.format(number["from"]["first_name"] + (number["from"]["last_name"] or '')),
            reply_markup=start_kb)

        update_table(category=data["category"],
                     option=data["option"],
                     number=number["contact"]["phone_number"],
                     text=data['text'] if type(data['text']) == str else "\n".join(data['text']),
                     order=data["order"])
