from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)


# Клавиатура для выбора пола
kb_gender = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='👨🏻‍️ Я парень', callback_data='male')],
        [InlineKeyboardButton(text='👩🏻‍️ Я девушка', callback_data='female')]
    ]
)


# Клавиатура для выбора рода занятий
kb_profession = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🎓 Я студент', callback_data='student')],
        [InlineKeyboardButton(text='💼 Я предприниматель', callback_data='businessman')],
        [InlineKeyboardButton(text='🏢 Работаю в найме', callback_data='employee')],
        [InlineKeyboardButton(text='🖥️ Фрилансер', callback_data='freelancer')]
    ]
)


# Клавиатура для выбора возрастной группы
kb_age = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='18 – 24', callback_data='age_18_24')],
        [InlineKeyboardButton(text='25 – 27', callback_data='age_25_27')],
        [InlineKeyboardButton(text='28 – 40', callback_data='age_28_40')],
        [InlineKeyboardButton(text='41 – 55', callback_data='age_41_55')],
        [InlineKeyboardButton(text='55+', callback_data='age_55_plus')],
    ]
)