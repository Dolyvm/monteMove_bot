import json

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InputFile

from admin_keyboards import ap_master_start_kb, ap_start_kb, ap_settings_kb
from functions import kb_from_dict, get_masters, update_masters, get_dosug, update_dosug
from statistics.stats_functions import create_month_stats

admins = [714799964, 347249536, 5614412865, 390167084, 2129598034, 359789155]


def edit_tab_name(tab, name):
    with open('masters.json', encoding='utf-8') as d:
        d = json.load(d)
    d[name] = d[tab]
    del d[tab]
    with open('masters.json', 'w', encoding='utf-8') as doc:
        json.dump(d, doc, ensure_ascii=False)


class AdminPanelStates(StatesGroup):
    AP_START_STATE = State()
    AP_SETTINGS_OPTION = State()
    GET_NEW_FIELD_STATE = State()
    CHOOSE_FIELD_STATE = State()
    GET_NEW_FIELD_NAME_STATE = State()

    AP_MASTER_START_STATE = State()
    GET_NEW_TAB_NAME_STATE = State()
    GET_NEW_MASTER_NAME_STATE = State()
    CHOOSE_TAB_STATE = State()
    CHOOSE_MASTER_STATE = State()


def register_admin_handlers(dp: Dispatcher):
    # @dp.message_handler(lambda message: message.chat.id in admins, commands=['open_panel'], state='*')
    @dp.message_handler(commands=['open_panel'], state='*', chat_id=admins)
    async def open_panel(message: Message):
        await message.answer(text="Что вы хотите сделать?", reply_markup=ap_start_kb)
        await AdminPanelStates.AP_START_STATE.set()

    @dp.callback_query_handler(state=AdminPanelStates.AP_START_STATE)
    async def ap_choose_start_option(callback: CallbackQuery, state: FSMContext):
        if callback.data == "check_stats":
            create_month_stats()
            await callback.message.answer_photo(photo=InputFile('statistics/stats.png'))
            return
        await state.update_data(file=callback.data)  # callback.data == 'master' | 'dosug'
        await callback.message.answer(text="Выберите подходящую опцию.", reply_markup=ap_settings_kb)
        await AdminPanelStates.AP_SETTINGS_OPTION.set()

    @dp.callback_query_handler(state=AdminPanelStates.AP_SETTINGS_OPTION)
    async def ap_choose_settings_option(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        kb = kb_from_dict(get_masters() if data["file"] == "master" else get_dosug())
        await state.update_data(option=callback.data)

        if callback.data == "add_tab":
            await callback.message.edit_text(text="Введите название новой вкладки")
            await AdminPanelStates.GET_NEW_TAB_NAME_STATE.set()
        elif callback.data == "add_field":
            await callback.message.edit_text(text="Выберите вкладку, в которой находится поле",
                                             reply_markup=kb)
            await AdminPanelStates.CHOOSE_TAB_STATE.set()
        elif callback.data == "edit_field":
            await callback.message.edit_text(text="Выберите вкладку, в которой находится поле",
                                             reply_markup=kb)
            await AdminPanelStates.CHOOSE_TAB_STATE.set()
        elif callback.data == "remove_field":
            await callback.message.edit_text(text="Выберите вкладку, в которой находится поле",
                                             reply_markup=kb)
            await AdminPanelStates.CHOOSE_TAB_STATE.set()
        elif callback.data == "edit_tab":
            await callback.message.edit_text(text="Выберите вкладку, название которой хотите изменить",
                                             reply_markup=kb)
            await AdminPanelStates.CHOOSE_TAB_STATE.set()
        elif callback.data == "remove_tab":
            await callback.message.edit_text(text="Выберите вкладку, которую хотите удалить",
                                             reply_markup=kb)
            await AdminPanelStates.CHOOSE_TAB_STATE.set()

    @dp.callback_query_handler(state=AdminPanelStates.CHOOSE_TAB_STATE)
    async def ap_choose_tab(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        await state.update_data(current_tab=callback.data)

        # Если нужно провести какие-либо изменения с вкладками
        if data['option'] == "edit_tab":
            await callback.message.edit_text("Введите новое название вкладки")
            await AdminPanelStates.GET_NEW_FIELD_STATE.set()
            return

        _dict = get_masters() if data["file"] == "master" else get_dosug()
        if data['option'] == "remove_tab":
            del _dict[callback.data]
            update_masters(_dict) if data["file"] == "master" else update_dosug(_dict)
            await callback.message.answer("Отлично! Вкладка удалена.")
            # Перекидываем в начало
            await callback.message.answer(text="Что вы хотите сделать?", reply_markup=ap_settings_kb)
            await AdminPanelStates.AP_SETTINGS_OPTION.set()
            return

        if data['option'] == "add_field":
            await callback.message.answer(text="Введите название поля и информацию о нем в следующем виде:\n"
                                               "Название поля\n"
                                               "Информация (на следующей строке)")
            await state.update_data(current_tab=callback.data)
            await AdminPanelStates.GET_NEW_FIELD_STATE.set()
            return

        kb = kb_from_dict(_dict[callback.data])
        if kb:
            await callback.message.edit_text(text='Список полей:',
                                             reply_markup=kb)
        else:
            await callback.message.edit_text(text="В этой вкладке отсутствуют поля.")

        await AdminPanelStates.CHOOSE_FIELD_STATE.set()

    @dp.callback_query_handler(state=AdminPanelStates.CHOOSE_FIELD_STATE)
    async def ap_choose_field(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        _dict = get_masters() if data["file"] == "master" else get_dosug()
        if data['option'] == 'edit_master':
            await callback.message.answer(text=f"```\n{callback.data}\n"
                                               f"{_dict[data['current_tab']][callback.data]}```\n"
                                               f"Введите новое название и описание мастера.", parse_mode="Markdown")
            await state.update_data(field=callback.data)
            await AdminPanelStates.GET_NEW_FIELD_NAME_STATE.set()
        elif data['option'] == "remove_master":
            del _dict[data['current_tab']][callback.data]
            update_masters(_dict) if data["file"] == "master" else update_dosug(_dict)

            await callback.message.answer("Поле успешно удалено.")
            # Перекидываем в начало
            await callback.message.answer(text="Что вы хотите сделать?", reply_markup=ap_settings_kb)
            await AdminPanelStates.AP_SETTINGS_OPTION.set()

    @dp.message_handler(state=AdminPanelStates.GET_NEW_TAB_NAME_STATE)
    async def get_new_tab(message: Message, state: FSMContext):
        data = await state.get_data()
        _dict = get_masters() if data["file"] == "master" else get_dosug()
        # Если нужно изменить название вкладки:
        if data.get('option') == "edit_tab":
            _dict[message.text] = _dict[data['current_tab']]
            del _dict[data['current_tab']]
            update_masters(_dict) if data["file"] == "master" else update_dosug(_dict)
            await message.answer("Отлично! Вкладка переименована.")
            # Перекидываем в начало
            await message.answer(text="Что вы хотите сделать?", reply_markup=ap_master_start_kb)
            await AdminPanelStates.AP_START_STATE.set()
            return

        # Сохраняем
        _dict[message.text] = {}
        update_masters(_dict) if data["file"] == "master" else update_dosug(_dict)

        await message.answer(text="Отлично! Новая вкладка успешно создана.")
        await message.answer(text="Введите название поля и информацию о нем в следующем виде:\n"
                                  "Название поля\n"
                                  "Информация (на следующей строке)")
        await state.update_data(current_tab=message.text)
        await AdminPanelStates.GET_NEW_FIELD_NAME_STATE.set()

    @dp.message_handler(state=AdminPanelStates.GET_NEW_FIELD_NAME_STATE)
    async def get_new_field_info(message: Message, state: FSMContext):
        try:
            field_name, field_info = message.text.split('\n', maxsplit=1)
        except ValueError:
            await message.answer(text="Сообщение написано неверно. Пожалуйста, попробуйте еще раз")
            return

        data = await state.get_data()
        _dict = get_masters() if data["file"] == "master" else get_dosug()
        if data.get("option") == "edit_master":
            del _dict[data["current_tab"]][data['master']]
        _dict[data["current_tab"]][field_name] = field_info

        update_masters(_dict) if data["file"] == "master" else update_dosug(_dict)
        await message.answer(
            text=f'Отлично! Информация о новом поле успешно добавлена во вкладку «{data["current_tab"]}»')

        # Перекидываем в начало
        await message.answer(text="Что вы хотите сделать?", reply_markup=ap_master_start_kb)
        await AdminPanelStates.AP_START_STATE.set()
