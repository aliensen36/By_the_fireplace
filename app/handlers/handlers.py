from aiogram.types import (FSInputFile, Message)
from aiogram import F, Router, types
import app.keyboards.reply as reply_kb
import app.keyboards.inline as inline_kb

router = Router()


# Обработчик кнопки '🍽️ У камина'
@router.message(F.text == '🍽️  У камина')
async def restaurant_description(message: Message):
    link = "https://telegra.ph/MYZHENATY-03-11-2"
    await message.answer(link, parse_mode='Markdown',
                         reply_markup=reply_kb.main)


# Обработчик кнопки '📋️ Меню'
@router.message(F.text == '📋️  Меню')
async def show_menu_options(message: Message):
    await message.answer("Выберите нужное вам меню👇",
                         reply_markup=reply_kb.menu_options_keyboard)


# Обработчик кнопки '🍽️ Основное меню'
@router.message(F.text == '🍽️ Основное меню')
async def send_main_menu_pdf(message: types.Message):
    file_path = 'docs/Main_menu.pdf'
    pdf = FSInputFile(path=file_path, filename='Main_menu.pdf')
    await message.answer_document(document=pdf,
                                  caption="Основное меню центрального зала")


# Обработчик кнопки '👶 Детское меню'
@router.message(F.text == '👶 Детское меню')
async def show_menu_kids(message: Message):
    link = "https://disk.yandex.ru/i/Qat0Y1HO88Arvw"
    await message.answer(link, parse_mode='Markdown',
                         reply_markup=reply_kb.menu_options_keyboard)


# Обработчик кнопки '⬅️ Назад'
@router.message(F.text == '⬅️ Назад')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите нужное вам действие👇",
                         reply_markup=reply_kb.main)

