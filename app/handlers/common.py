from aiogram.fsm.context import FSMContext
from aiogram.types import (FSInputFile, Message, InlineKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram import F, Router, types, Bot
import app.keyboards.reply as reply_kb
from app.text import *


router = Router()


# Обработчик кнопки '🍽️ У камина'
@router.message(F.text == '🍽️ У камина')
async def restaurant_description(message: Message):
    link = "https://telegra.ph/MYZHENATY-03-11-2"
    await message.answer(link, parse_mode='Markdown',
                         reply_markup=reply_kb.main)


# Обработчик кнопки '📋️ Меню'
@router.message(F.text == '📋️ Меню')
async def show_menu_options(message: Message):
    await message.answer("Выберите нужное вам меню👇",
                         reply_markup=reply_kb.kb_menu_options)


# Обработчик кнопки '🍽️ Основное меню'
@router.message(F.text == '🍽️ Основное меню')
async def send_main_menu_pdf(message: Message):
    file_path = 'docs/Main_menu.pdf'
    pdf = FSInputFile(path=file_path, filename='Main_menu.pdf')
    await message.answer_document(document=pdf,
                                  caption="Основное меню центрального зала",
                                  reply_markup=reply_kb.kb_menu_options)


# Обработчик кнопки '👶 Детское меню'
@router.message(F.text == '👶 Детское меню')
async def show_menu_kids(message: Message):
    link = "https://disk.yandex.ru/i/Qat0Y1HO88Arvw"
    await message.answer(link, parse_mode='Markdown',
                         reply_markup=reply_kb.kb_menu_options)


# Обработчик кнопки '⬅️ Назад'
@router.message(F.text == '⬅️ Назад')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите 👇",
                         reply_markup=reply_kb.main)


# Обработчик кнопки '📍 Путь к нам'
@router.message(F.text == '📍️ Путь к нам')
async def location(message: Message):
    address = "г. Москва, ул. Лесная, д. 10"
    await message.answer(f"📍 Наш адрес: {address}")
    latitude = 55.778644  # Широта
    longitude = 37.589410  # Долгота
    await message.answer_location(latitude=latitude, longitude=longitude)


# Обработчик кнопки '🚚️ Доставка'
@router.message(F.text == '🚚️ Доставка')
async def delivery(message: Message):
    text = "🍽️ Закажите любое блюдо домой или в офис 🍴\n\nhttps://restoranmyzhenaty.ru/"
    await message.answer(text)




# Обработчик кнопки 'Отмена'
@router.message(F.text == 'Отмена')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите 👇",
                         reply_markup=reply_kb.main)
