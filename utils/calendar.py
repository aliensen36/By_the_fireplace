import calendar
from datetime import datetime, date
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MONTH_NAMES = [
    "Январь", "Февраль", "Март", "Апрель",
    "Май", "Июнь", "Июль", "Август",
    "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
]

def get_calendar(year=None, month=None):
    if year is None or month is None:
        now = datetime.now()
        year = now.year
        month = now.month

    today = date.today()
    keyboard: list[list[InlineKeyboardButton]] = []

    # Название месяца
    keyboard.append([
        InlineKeyboardButton(text=f"{MONTH_NAMES[month - 1]} {year}", callback_data="ignore")
    ])

    # Дни недели
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    keyboard.append([
        InlineKeyboardButton(text=day, callback_data="ignore") for day in days
    ])

    # Дни месяца
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.itermonthdays(year, month)

    week = []
    for day in month_days:
        if day == 0:
            week.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
        else:
            button_date = date(year, month, day)
            if button_date < today:
                # Прошедшие дни — неактивные
                week.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
            else:
                # Активные будущие и сегодняшние дни
                date_str = f"{day:02d}.{month:02d}.{year}"
                week.append(InlineKeyboardButton(text=str(day), callback_data=f"select_date:{date_str}"))

        if len(week) == 7:
            keyboard.append(week)
            week = []

    if week:
        while len(week) < 7:
            week.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
        keyboard.append(week)

    # Навигация
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    keyboard.append([
        InlineKeyboardButton(text="« Пред", callback_data=f"prev_month:{prev_month}:{prev_year}"),
        InlineKeyboardButton(text="След »", callback_data=f"next_month:{next_month}:{next_year}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
