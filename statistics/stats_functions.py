import calendar
import datetime
import json

import pandas as pd

calendar = calendar.Calendar()


def get_stats() -> dict:
    with open("statistics/statistics.json") as stats:
        return json.load(stats)


def upload_stats(new_stats):
    with open("statistics/statistics.json", 'w') as stats:
        json.dump(new_stats, stats)


def get_today_visitors():
    with open("statistics/today_visitors.json") as data:
        return json.load(data)


def append_visitor(user_id):
    visitors = get_today_visitors()
    if user_id not in visitors:
        visitors.append(user_id)
        with open("statistics/today_visitors.json", "w") as data:
            json.dump(visitors, data)
        update_stats()


def remove_visitors():
    with open("statistics/today_visitors.json", "w") as data:
        json.dump(list(), data)


def build_year_stats(year):
    year = int(year)
    new_stats = {str(year): {}}
    for month in range(1, 13):
        for week in calendar.monthdayscalendar(year, month):
            for day in week:
                if day:
                    if f"{month:0>2}" not in new_stats[str(year)]:
                        new_stats[str(year)][f"{month:0>2}"] = {}
                    new_stats[str(year)][f"{month:0>2}"][f"{day:0>2}"] = 0
    return new_stats


def update_stats():
    stats = get_stats()
    today: datetime.date = datetime.date.today()
    year, month, day = map(lambda x: f"{x:0>2}", (today.year, today.month, today.day))
    if str(year) not in stats:
        stats[str(year)] = build_year_stats(year)
    stats[year][month][day] += 1
    upload_stats(stats)


def create_month_stats(year=None, month=None):
    today = datetime.date.today()
    if year is None:
        year, month = today.year, today.month
    stats = get_stats()[str(year)][f"{month:0>2}"]
    stats = {key: value for key, value in list(stats.items())[:today.day]}
    df = pd.Series(stats, dtype='int8')
    df.plot(ylabel="Количество уникальных пользователей", xlabel="День", grid=True).figure.savefig('statistics/stats.png')
    print(f"Статистика на {year}.{month} создана.")


def test():
    create_month_stats(2023, 1)
    pass


if __name__ == "__main__":
    test()
