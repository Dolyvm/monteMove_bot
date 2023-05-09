import random
import json

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_order():
    # column = worksheet.col_values(4)
    # while True:
    #     order = random.randint(100000, 999999)
    #     if order not in column:
    #         return order
    return random.randint(100000, 999999)


def get_file(filename: str) -> dict:
    with open(f'files/{filename}.json', encoding='utf-8') as d:
        return json.load(d)


def update_file(filename: str, new_dict: dict):
    with open(f'files/{filename}.json', 'w', encoding='utf-8') as d:
        json.dump(new_dict, d, ensure_ascii=False)


def kb_from_dict(d: dict):
    if d.keys():
        return InlineKeyboardMarkup(row_width=1).add(*[InlineKeyboardButton(text=i, callback_data=i)
                                                       for i in d.keys()])
    else:
        return


translit_dict = {
        "у":"y",
        "К":"K",
        "Е":"E",
        "е":"e",
        "Н":"H",
        "х":"x",
        "Х":"X",
        "В":"B",
        "а":"a",
        "А":"A",
        "р":"p",
        "Р":"P",
        "о":"o",
        "О":"O",
        "с":"c",
        "С":"C",
        "М":"M",
        "Т":"T"
    }


def compress_text(text: str) -> str:
    result = ""
    for c in text:
        result += translit_dict.get(c, c)
    return result
