#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gspread
import random
from datetime import datetime

gc = gspread.service_account(filename="credit.json")

sh = gc.open("Все заявки")

worksheet = sh.get_worksheet(0)


def generateOrder():
    column = worksheet.col_values(4)
    while True:
        order = random.randint(100000, 999999)
        if order not in column:
            return order


def update_table(category, option, number, text, order, client_nickname="", ):
    # new_n = len(worksheet.col_values("1")) + 1  # Порядковый номер нового заказа
    # for i, arg in enumerate(args, start=1):
    #     worksheet.update_cell(new_n, i, arg)
    #     print('записано:', i, arg)
    new_n = len(worksheet.col_values("1")) + 1  # Порядковый номер нового заказа
    worksheet.update_cell(new_n, 1, datetime.now().strftime("%d.%m.%Y"))
    worksheet.update_cell(new_n, 2, category)
    worksheet.update_cell(new_n, 3, option)
    worksheet.update_cell(new_n, 6, client_nickname)
    worksheet.update_cell(new_n, 7, number)
    worksheet.update_cell(new_n, 8, text)
    worksheet.update_cell(new_n, 9, order)


"""update_table(data["category"],
                     data["option"],
                     number["contact"]["phone_number"],
                     data['text'] if type(data['text']) == str else "\n".join(data['text']),
                     data["order"])"""


def test():
    new_n = len(worksheet.col_values("1")) + 1  # Порядковый номер нового заказа
    worksheet.update_cell(new_n, 1, datetime.now().strftime("%d.%m.%Y"))
    worksheet.update_cell(new_n, 2, "ВНЖ")
    worksheet.update_cell(new_n, 3, "ВНЖ")
    worksheet.update_cell(new_n, 6, "@huseeads")
    worksheet.update_cell(new_n, 7, "898515888026")
    worksheet.update_cell(new_n, 8, "test")
    worksheet.update_cell(new_n, 9, "123456")


if __name__ == "__main__":
    test()
