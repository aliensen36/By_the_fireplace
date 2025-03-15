from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Главная клавиатура
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🍽️ У камина'), KeyboardButton(text='📋️ Меню')],
    [KeyboardButton(text='📅🍽️ Забронировать стол')],
    [KeyboardButton(text='🚚️ Доставка'), KeyboardButton(text='📍️ Путь к нам')],
    [KeyboardButton(text='🎁️ Программа лояльности')],
    [KeyboardButton(text='📝 Оставить отзыв'), KeyboardButton(text='🛎️ Вызов официанта')],
    [KeyboardButton(text='📝 Заполнить анкету')],
],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие')



# Клавиатура для выбора меню ресторана
kb_menu_options = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🍽️ Основное меню')],
        [KeyboardButton(text='👶 Детское меню')],
        [KeyboardButton(text='⬅️ Назад')],
],
    resize_keyboard=True)


# Клавиатура для программы лояльности
kb_loyalty_program = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='💳 Карта лояльности')],
        [KeyboardButton(text='👥 Пригласи друга')],
        [KeyboardButton(text='⬅️ Назад')],
],
    resize_keyboard=True)


# Клавиатура для отзывов
kb_feedback = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='💬 Оставить отзыв')],
        [KeyboardButton(text='✉️ Написать директору')],
        [KeyboardButton(text='⬅️ Назад')],
],
    resize_keyboard=True)


# Кнопка "Отмена"
cancel_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отмена')],
],
    resize_keyboard=True)


def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (),
):
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:

            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)
