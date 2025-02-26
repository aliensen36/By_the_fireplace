# keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главная клавиатура
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


# Клавиатура для выбора меню
menu_options_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🍽️ Основное меню')],
        [KeyboardButton(text='👶 Детское меню')],
        [KeyboardButton(text='⬅️ Назад')],
],
    resize_keyboard=True)



# settings = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='YouTube', url='https://youtube.com')]
# ])