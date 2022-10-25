from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, MediaGroup

from functions import generate_order
from keyboards import start_kb, exchange_kb, residence_docs_kb, back_button, gruz_kb, realty_kb, trans_vis_kb
from utils import start_text, option_text, exchange_text, final_text, exchange_order_text, residence_docs_text, \
    gruz_text, realty_text_1, realty_text_2, realty_text_hand_over, trans_vis_text_1, trans_vis_text_2, trans_vis_text_3


class ChooseOptionsStates(StatesGroup):
    start_state = State()
    exchange_state = State()
    residence_state = State()
    rent_state = State()
    transfer_state = State()
    gruz_state = State()
    realty_state = State()
    final_state = State()


class FinalStates(StatesGroup):
    exchange_final_state = State()
    transfer_final_state = State()
    realty_final_stage = State()
    gruz_final_state = State()


def register_user_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start', 'help'], state='*')
    async def start(message: Message, state: FSMContext):
        await message.answer(start_text.format(message.chat.full_name), reply_markup=start_kb)
        await ChooseOptionsStates.start_state.set()

    @dp.callback_query_handler(state=ChooseOptionsStates.start_state)
    async def start_options(callback: CallbackQuery):
        match callback.data:
            case 'exchange':
                await callback.message.edit_text(option_text, reply_markup=exchange_kb)
                await ChooseOptionsStates.exchange_state.set()
            case 'residence/docs':
                await callback.message.edit_text(option_text, reply_markup=residence_docs_kb)
                await ChooseOptionsStates.residence_state.set()
            case 'rent_avt':
                ...
                await ChooseOptionsStates.rent_state.set()
            case 'transfer':
                await callback.message.edit_text(option_text, reply_markup=trans_vis_kb)
                await ChooseOptionsStates.transfer_state.set()
            case 'gruz':
                await callback.message.edit_text(option_text, reply_markup=gruz_kb)
                await ChooseOptionsStates.gruz_state.set()
            case 'realty':
                await callback.message.edit_text(option_text, reply_markup=realty_kb)
                await ChooseOptionsStates.realty_state.set()

    @dp.callback_query_handler(state=ChooseOptionsStates.exchange_state)
    async def exchange_options(callback: CallbackQuery):
        match callback.data:
            case 'back':
                await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                                 reply_markup=start_kb)
                await ChooseOptionsStates.start_state.set()
            case _:
                await callback.message.edit_text(exchange_text)
                await FinalStates.exchange_final_state.set()

    @dp.callback_query_handler(state=ChooseOptionsStates.transfer_state)
    async def transfer_options(callback: CallbackQuery):
        match callback.data:
            case 'back':
                await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                                 reply_markup=start_kb)
                await FinalStates.transfer_final_state.set()
            case 'meet_port':
                await callback.message.edit_text(trans_vis_text_1)
                await FinalStates.transfer_final_state.set()

            case 'from_c_to_c':
                await callback.message.edit_text(trans_vis_text_2)
                await FinalStates.transfer_final_state.set()

            case 'visarun':
                await callback.message.edit_text(trans_vis_text_3)
                await FinalStates.transfer_final_state.set()

    @dp.callback_query_handler(state=ChooseOptionsStates.realty_state)
    async def realty_options(callback: CallbackQuery):
        match callback.data:
            case 'back':
                await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                                 reply_markup=start_kb)
                await FinalStates.realty_final_stage.set()
            case 'rent':
                await callback.message.edit_text(realty_text_1)
                await FinalStates.realty_final_stage.set()

            case 'buy':
                await callback.message.edit_text(realty_text_2)
                await FinalStates.realty_final_stage.set()

            # Cдать
            case 'give_rent':
                await callback.message.edit_text(realty_text_2)
                await FinalStates.realty_final_stage.set()

            case 'sell':
                await callback.message.edit_text(realty_text_2)
                await FinalStates.realty_final_stage.set()

            case _:
                await callback.message.edit_text(realty_text_hand_over)
                await FinalStates.realty_final_stage.set()

    @dp.callback_query_handler(state=ChooseOptionsStates.residence_state)
    async def residence_options(callback: CallbackQuery):
        if callback.data == 'back':
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await ChooseOptionsStates.start_state.set()
        else:
            await callback.message.answer(text=residence_docs_text)
            await ChooseOptionsStates.final_state.set()

    @dp.callback_query_handler(state=ChooseOptionsStates.gruz_state)
    async def gruz_options(callback: CallbackQuery):
        if callback.data == 'back':
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await ChooseOptionsStates.start_state.set()
        else:
            await callback.message.answer(text=gruz_text)
            await FinalStates.gruz_final_state.set()

    @dp.message_handler(state=ChooseOptionsStates.final_state, content_types=('photo', 'text'))
    async def get_exchange_final(message: Message, state: FSMContext):
        order = generate_order()
        await message.answer(text=final_text.format(order))
        await message.answer(start_text.format(message.chat.full_name), reply_markup=start_kb)
        await ChooseOptionsStates.start_state.set()
        await message.bot.send_message(chat_id=-1001591695557, text=exchange_order_text.format(order, message.text))

    @dp.message_handler(state=FinalStates.realty_final_stage, content_types=('photo', 'text'))
    async def get_realty_final(message: Message, state: FSMContext):
        # TODO Прописать конец отправки фотографий по нажатии на соответствующую кнопку
        order = generate_order()
        await message.answer(text=final_text.format(order))
        await message.answer(start_text.format(message.chat.full_name), reply_markup=start_kb)
        await ChooseOptionsStates.start_state.set()
        await message.bot.send_photo(chat_id=-1001591695557,
                                     caption=exchange_order_text.format(order, message.caption or message.text),
                                     photo=message.media_group_id or message.photo[-1].file_id)
