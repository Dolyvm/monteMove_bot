from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from functions import generate_order
from keyboards import start_kb, exchange_kb, residence_docs_kb, back_button, gruz_kb, realty_kb, trans_vis_kb
from utils import start_text, option_text, exchange_text, exchange_final_text, exchange_order_text, residence_docs_text, \
    gruz_text, realty_text_1, realty_text_2, realty_text_hand_over, trans_vis_text_1, trans_vis_text_2, trans_vis_text_3


class UserStates(StatesGroup):
    start_state = State()
    exchange_state = State()
    residence_state = State()
    rent_state = State()
    transfer_state = State()
    gruz_state = State()
    realty_state = State()
    final_state = State()


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
                ...
                await UserStates.rent_state.set()
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
    async def exchange_options(callback: CallbackQuery):
        match callback.data:
            case 'back':
                await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                                 reply_markup=start_kb)
                await UserStates.start_state.set()
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
    async def exchange_options(callback: CallbackQuery):
        match callback.data:
            case 'back':
                await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                                 reply_markup=start_kb)
                await UserStates.start_state.set()
            case 'rent':
                await callback.message.edit_text(realty_text_1)
                await UserStates.final_state.set()
            case 'buy':
                await callback.message.edit_text(realty_text_2)
                await UserStates.final_state.set()
            case _:
                await callback.message.edit_text(realty_text_hand_over)
                await UserStates.final_state.set()

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
    async def residence_options(callback: CallbackQuery):
        if callback.data == 'back':
            await callback.message.edit_text(text=start_text.format(callback.message.chat.full_name),
                                             reply_markup=start_kb)
            await UserStates.start_state.set()
        else:
            await callback.message.answer(text=gruz_text)
            await UserStates.final_state.set()

    @dp.message_handler(state=UserStates.final_state, content_types= ('photo', 'text'))
    async def get_exchange_final(message: Message, state: FSMContext):
        order = generate_order()
        await message.answer(text=exchange_final_text.format(order))
        await message.answer(start_text.format(message.chat.full_name), reply_markup=start_kb)
        await UserStates.start_state.set()
        await message.bot.send_message(chat_id=-1001591695557, text=exchange_order_text.format(order, message.text))