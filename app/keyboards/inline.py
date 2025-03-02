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
        [InlineKeyboardButton(text="🎓 Я студент", callback_data="student")],
        [InlineKeyboardButton(text="💼 Я предприниматель", callback_data="businessman")],
        [InlineKeyboardButton(text="🏢 Работаю в найме", callback_data="employee")],
        [InlineKeyboardButton(text="🖥️ Фрилансер", callback_data="freelancer")]
    ]
)