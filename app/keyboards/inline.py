from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)


# Клавиатура для выбора пола
kb_gender = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='👨🏻‍️ Я парень', callback_data='gender_male')],
        [InlineKeyboardButton(text='👩🏻‍️ Я девушка', callback_data='gender_female')]
    ]
)


# Клавиатура для выбора рода занятий
kb_profession = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎓 Я студент", callback_data="profession_student")],
        [InlineKeyboardButton(text="💼 Я предприниматель", callback_data="profession_business")],
        [InlineKeyboardButton(text="🏢 Работаю в найме", callback_data="profession_employed")],
        [InlineKeyboardButton(text="🖥️ Фрилансер", callback_data="profession_freelancer")]
    ]
)