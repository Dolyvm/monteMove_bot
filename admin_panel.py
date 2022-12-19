import json
import aiogram
from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, MediaGroup, ReplyKeyboardRemove, \
    InlineKeyboardButton, Contact
from aiogram.utils.exceptions import ValidationError

from admin_keyboards import start_admin_kb, sphere_options_kb, ap_start_kb
from functions import kb_from_dict, get_masters, update_masters
from table_ctrl import generateOrder
from keyboards import start_kb, exchange_kb, residence_docs_kb, back_button, gruz_kb, realty_kb, trans_vis_kb, \
    realty_final_kb, residence_options_kb, open_company_kb, employer_kb, masters_kb, url_kb, auto_kb, number_request, \
    beauty_masters_kb
from table_ctrl import update_table
from utils import start_text, option_text, exchange_text, final_text, exchange_order_text, residence_docs_text, \
    gruz_text, realty_text_1, realty_text_2, trans_vis_text_1, trans_vis_text_2, trans_vis_text_3, realty_text_3, \
    realty_text_4, buttons_name_dict, vnj_text, employer_text, vnj_docs_text, zaglushka_text, byt_text, \
    rent_auto_first_text, rent_auto_second_text, rent_auto_third_text, number_text, beauty_text, other_text

admins = []


def edit_tab_name(tab, name):
    with open('masters.json', encoding='utf-8') as d:
        d = json.load(d)
    d[name] = d[tab]
    del d[tab]
    with open('masters.json', 'w', encoding='utf-8') as doc:
        json.dump(d, doc, ensure_ascii=False)


class AdminPanelStates(StatesGroup):
    AP_START_STATE = State()
    GET_NEW_TAB_NAME_STATE = State()
    GET_NEW_MASTER_NAME_STATE = State()
    CHOOSE_TAB_STATE = State()
    CHOOSE_MASTER_STATE = State()


def register_admin_handlers(dp: Dispatcher):
    # @dp.message_handler(lambda message: message.chat.id in admins, commands=['open_panel'], state='*')
    @dp.message_handler(commands=['open_panel'], state='*')
    async def open_panel(message: Message, state: FSMContext):
        await message.answer(text="Что вы хотите сделать?", reply_markup=ap_start_kb)
        await AdminPanelStates.AP_START_STATE.set()

    @dp.callback_query_handler(state=AdminPanelStates.AP_START_STATE)
    async def ap_choose_option(callback: CallbackQuery, state: FSMContext):
        match callback.data:
            case "add_tab":
                await callback.message.edit_text(text="Введите название новой вкладки")
                await AdminPanelStates.GET_NEW_TAB_NAME_STATE.set()
            case "add_master":
                await state.update_data(option="add_master")
                await callback.message.edit_text(text="Выберите вкладку, в которой находится мастер",
                                                 reply_markup=kb_from_dict(get_masters()))
                await AdminPanelStates.CHOOSE_TAB_STATE.set()
            case "edit_master":
                await state.update_data(option="edit_master")
                await callback.message.edit_text(text="Выберите вкладку, в которой находится мастер",
                                                 reply_markup=kb_from_dict(get_masters()))
                await AdminPanelStates.CHOOSE_TAB_STATE.set()
            case "remove_master":
                await state.update_data(option="remove_master")
                await callback.message.edit_text(text="Выберите вкладку, в которой находится мастер",
                                                 reply_markup=kb_from_dict(get_masters()))
                await AdminPanelStates.CHOOSE_TAB_STATE.set()
            case "edit_tab":
                await state.update_data(option="edit_tab")
                await callback.message.edit_text(text="Выберите вкладку, название которой хотите изменить",
                                                 reply_markup=kb_from_dict(get_masters()))
                await AdminPanelStates.CHOOSE_TAB_STATE.set()
            case "remove_tab":
                await state.update_data(option="remove_tab")
                await callback.message.edit_text(text="Выберите вкладку, которую хотите удалить",
                                                 reply_markup=kb_from_dict(get_masters()))
                await AdminPanelStates.CHOOSE_TAB_STATE.set()

    @dp.callback_query_handler(state=AdminPanelStates.CHOOSE_TAB_STATE)
    async def ap_choose_tab(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        await state.update_data(current_tab=callback.data)

        # Если нужно провести какие-либо изменения с вкладками
        if data['option'] == "edit_tab":
            await callback.message.edit_text("Введите новое название вкладки")
            await AdminPanelStates.GET_NEW_TAB_NAME_STATE.set()
            return

        masters = get_masters()
        if data['option'] == "remove_tab":
            del masters[callback.data]
            update_masters(masters)
            await callback.message.answer("Отлично! Вкладка удалена.")
            # Перекидываем в начало
            await callback.message.answer(text="Что вы хотите сделать?", reply_markup=ap_start_kb)
            await AdminPanelStates.AP_START_STATE.set()
            return

        if data['option'] == "add_master":
            await callback.message.answer(text="Введите название мастера и информацию о нем в следующем виде:\n"
                                      "Название мастера\n"
                                      "Информация (на следующей строке)")
            await state.update_data(current_tab=callback.data)
            await AdminPanelStates.GET_NEW_MASTER_NAME_STATE.set()
            return

        kb = kb_from_dict(masters[callback.data])
        if kb:
            await callback.message.edit_text(text='Список мастеров:',
                                             reply_markup=kb)
        else:
            await callback.message.edit_text(text="В этой вкладке отсутствуют мастера.")

        await AdminPanelStates.CHOOSE_MASTER_STATE.set()

    @dp.callback_query_handler(state=AdminPanelStates.CHOOSE_MASTER_STATE)
    async def ap_choose_master(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        masters = get_masters()
        match data['option']:
            case "edit_master":
                await callback.message.answer(text=f"```\n{callback.data}\n"
                                                   f"{masters[data['current_tab']][callback.data]}```\n"
                                                   f"Введите новое название и описание мастера.", parse_mode="Markdown")
                await state.update_data(master=callback.data)
                await AdminPanelStates.GET_NEW_MASTER_NAME_STATE.set()
            case "remove_master":
                del masters[data['current_tab']][callback.data]
                update_masters(masters)

                await callback.message.answer("Мастер успешно удален.")
                # Перекидываем в начало
                await callback.message.answer(text="Что вы хотите сделать?", reply_markup=ap_start_kb)
                await AdminPanelStates.AP_START_STATE.set()

    @dp.message_handler(state=AdminPanelStates.GET_NEW_TAB_NAME_STATE)
    async def get_new_tab(message: Message, state: FSMContext):
        data = await state.get_data()
        masters = get_masters()
        # Если нужно изменить название вкладки:
        if data.get('option') == "edit_tab":
            masters[message.text] = masters[data['current_tab']]
            del masters[data['current_tab']]
            update_masters(masters)
            await message.answer("Отлично! Вкладка переименована.")
            # Перекидываем в начало
            await message.answer(text="Что вы хотите сделать?", reply_markup=ap_start_kb)
            await AdminPanelStates.AP_START_STATE.set()
            return

        # Сохраняем
        masters[message.text] = {}
        update_masters(masters)
        await message.answer(text="Отлично! Новая вкладка успешно создана.")
        await message.answer(text="Введите название мастера и информацию о нем в следующем виде:\n"
                                  "Название мастера\n"
                                  "Информация (на следующей строке)")
        await state.update_data(current_tab=message.text)
        await AdminPanelStates.GET_NEW_MASTER_NAME_STATE.set()

    @dp.message_handler(state=AdminPanelStates.GET_NEW_MASTER_NAME_STATE)
    async def get_new_master_info(message: Message, state: FSMContext):
        try:
            master_name, master_info = message.text.split('\n', maxsplit=1)
        except ValueError:
            await message.answer(text="Сообщение написано неверно. Пожалуйста, попробуйте еще раз")
            return

        data = await state.get_data()
        d = get_masters()
        if data.get("option") == "edit_master":
            del d[data["current_tab"]][data['master']]
        d[data["current_tab"]][master_name] = master_info

        update_masters(d)
        await message.answer(
            text=f'Отлично! Информация о новом мастере успешно добавлена во вкладку «{data["current_tab"]}»')

        # Перекидываем в начало
        await message.answer(text="Что вы хотите сделать?", reply_markup=ap_start_kb)
        await AdminPanelStates.AP_START_STATE.set()

