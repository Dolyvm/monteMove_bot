#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gspread
import random

gc = gspread.oauth(credentials_filename="credentials.json")

sh = gc.open("MonteMove")

worksheet = sh.get_worksheet(9)


def generateOrder():
    column = worksheet.col_values(4)
    while True:
        order = random.randint(100000, 999999)
        if order not in column:
            return order


def update_table(*args):
    assert len(args) == 5, "Недостаточно аргументов"
    new_n = len(worksheet.col_values("1")) + 1  # Порядковый номер нового заказа
    for i, arg in enumerate(args, start=1):
        worksheet.update_cell(new_n, i, arg)


def get_line(number: str, answer="line"):
    number = number[1:] if number[0] == "+" else number
    values = worksheet.col_values(3)
    line = len(values) - values[::-1].index(number)
    return line if answer == "line" else worksheet.cell(line, 4).value


def checkPayment():
    for i in range(1, len(worksheet.col_values(1)) + 1):
        values = worksheet.row_values(i)
        if (values[7], values[8]) == ("Оплачено.", "Не обработано."):
            worksheet.update_cell(i, 9, "Обработано.")
            yield values[9], values[3]


def test():
    print(worksheet.col_values(1))


if __name__ == "__main__":
    test()