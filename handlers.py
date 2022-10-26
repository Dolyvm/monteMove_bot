from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, MediaGroup, ReplyKeyboardRemove

from functions import generate_order
from keyboards import start_kb, exchange_kb, residence_docs_kb, back_button, gruz_kb, realty_kb, trans_vis_kb, \
    realty_final_kb
from utils import start_text, option_text, exchange_text, final_text, exchange_order_text, residence_docs_text, \
    gruz_text, realty_text_1, realty_text_2, trans_vis_text_1, trans_vis_text_2, trans_vis_text_3, realty_text_3, \
    realty_text_4


class UserStates(StatesGroup):
    start_state = State()
    exchange_state = State()
    residence_state = State()
    rent_state = State()
    transfer_state = State()
    gruz_state = State()
    realty_state = State()
    final_state = State()
    realty_final_state = State()


def register_user_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start', 'help'], state='*')
    async def start(message: Message, state: FSMContext):
        await message.answer(start_text.format(message.chat.full_name), reply_markup=start_kb)
        await UserStates.start_state.set()

    @dp.callback_query_handler(state=UserStates.start_state)
    async def start_options(callback: CallbackQuery):
        match callback.data:
            case 'exchange':
                await callback.message.edit_text(option_text, reply_markup=exchange_kb)
                await UserStates.exchange_state.set()
            case 'residence/docs':
                await callback.message.edit_text(option_text, reply_markup=residence_docs_kb)
                await UserStates.residence_state.set()
            case 'rent_avt':
                await callback.answer()
                # await UserStates.rent_state.set()
            case 'transfer':
                await callback.message.edit_text(option_text, reply_markup=trans_vis_kb)
                await UserStates.transfer_state.set()
            case 'gruz':
                await callback.message.edit_text(option_text, reply_markup=gruz_kb)
                await UserStates.gruz_state.set()
            case 'realty':
                await callback.message.edit_text(option_text, reply_markup=realty_kb)
                await UserStates.realty_state.set()

    @dp.callback_query_handler(state=UserStates.exchange_state)
    async def exchange_options(callback: CallbackQuery):
        match callback.data:
            case 'back':
                await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                                 reply_markup=start_kb)
                await UserStates.start_state.set()
            case _:
                await callback.message.edit_text(exchange_text)
                await UserStates.final_state.set()

    @dp.callback_query_handler(state=UserStates.transfer_state)
    async def transfer_options(callback: CallbackQuery):
        match callback.data:
            case 'back':
                await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                                 reply_markup=start_kb)
                await   UserStates.final_state.set()
            case 'meet_port':
                await callback.message.edit_text(trans_vis_text_1)
                await UserStates.final_state.set()

            case 'from_c_to_c':
                await callback.message.edit_text(trans_vis_text_2)
                await UserStates.final_state.set()

            case 'visarun':
                await callback.message.edit_text(trans_vis_text_3)
                await UserStates.final_state.set()

    @dp.callback_query_handler(state=UserStates.realty_state)
    async def realty_options(callback: CallbackQuery):
        match callback.data:
            case 'back':
                await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                                 reply_markup=start_kb)
                await UserStates.final_state.set()
            case 'rent':
                await callback.message.edit_text(realty_text_1)
                await UserStates.final_state.set()

            case 'buy':
                await callback.message.edit_text(realty_text_2)
                await UserStates.final_state.set()

            # Cдать
            case 'give_rent':
                await callback.message.answer(realty_text_3, reply_markup=realty_final_kb)
                await UserStates.realty_final_state.set()

            case 'sell':
                await callback.message.answer(realty_text_4, reply_markup=realty_final_kb)
                await UserStates.realty_final_state.set()

    @dp.callback_query_handler(state=UserStates.residence_state)
    async def residence_options(callback: CallbackQuery):
        if callback.data == 'back':
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await UserStates.start_state.set()
        else:
            await callback.message.answer(text=residence_docs_text)
            await UserStates.final_state.set()

    @dp.callback_query_handler(state=UserStates.gruz_state)
    async def gruz_options(callback: CallbackQuery):
        if callback.data == 'back':
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await UserStates.start_state.set()
        else:
            await callback.message.answer(text=gruz_text)
            await UserStates.final_state.set()

    @dp.message_handler(state=UserStates.final_state, content_types=('photo', 'text'))
    async def get_exchange_final(message: Message, state: FSMContext):
        order = generate_order()
        await message.answer(text=final_text.format(order))
        await message.answer(start_text.format(message.chat.full_name), reply_markup=start_kb)
        await UserStates.start_state.set()
        await message.bot.send_message(chat_id=-1001591695557, text=exchange_order_text.format(order, message.text))

    @dp.message_handler(state=UserStates.realty_final_state, content_types=('photo', 'text'))
    async def get_realty_files(message: Message, state: FSMContext):
        if message.text == 'Завершить отправку файлов':
            order = generate_order()
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
            await message.bot.send_message(chat_id=-1001591695557, text=exchange_order_text.format(order, data['text']))
            await message.bot.send_media_group(chat_id=-1001591695557, media=media)
            await message.answer(text=final_text.format(order), reply_markup=ReplyKeyboardRemove())
            await state.update_data(photos=[])
            await state.update_data(text=None)
            await UserStates.start_state.set()
            await message.answer(start_text.format(message.chat.full_name), reply_markup=start_kb)
        elif message.text:
            await state.update_data(text=message.text)
        elif message.photo:
            data = await state.get_data()
            photos: list = data.get('photos', [])
            photos.append(message.photo[-1].file_id)
            await state.update_data(photos=photos)
        elif message.caption:
            await state.update_data(text=message.text)
