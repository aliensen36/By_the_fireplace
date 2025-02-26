# keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# start_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="🚀 Старт")]
#     ],
#     resize_keyboard=True
# )



main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🍽️  У камина'), KeyboardButton(text='📋️  Меню')],
    [KeyboardButton(text='📅🍽️  Забронировать стол')],
    [KeyboardButton(text='🚚️  Доставка'), KeyboardButton(text='📍️  Путь к нам')],
    [KeyboardButton(text='🎁️  Программа лояльности')],
    [KeyboardButton(text='️📝  Оставить отзыв'), KeyboardButton(text='🛎️  Вызов официанта')],
    [KeyboardButton(text='📝  Заполнить анкету')],
],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие')

# settings = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='YouTube', url='https://youtube.com')]
# ])