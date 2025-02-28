# handlers.py

import os
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import (Message, BotCommand, InputFile, BufferedInputFile,
                           FSInputFile, InputFile, CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
from aiogram import F, Router, Bot, Dispatcher, types
import app.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from app.fsm_states import InitialRegistration

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    # Обработка отсутствия username
    if not message.from_user.username:
        photo_ios_path = 'docs/ios_guide.jpg'
        photo_android_path = 'docs/android_guide.jpg'
        ios_instructions = (
            "📱 **IOS**\n\n"
            "1. Нажмите ⚙️Настройки в правом нижнем углу\n"
            "2. Нажмите \"Выбрать имя пользователя\"\n"
            "3. Введите имя пользователя\n"
        )
        android_instructions = (
            "🤖 **Android**\n\n"
            "1. Нажмите на 3 полоски в левом верхнем углу\n"
            "2. Нажмите ⚙️Настройки\n"
            "3. Нажмите на \"Имя пользователя\" и введите имя\n"
        )
        await message.answer_photo(photo=types.FSInputFile(photo_ios_path),
                                 caption=ios_instructions)
        await message.answer_photo(photo=types.FSInputFile(photo_android_path),
                                 caption=android_instructions)
        await message.answer("Для взаимодействия с ботом необходимо задать "
                             "**Username** в настройках Telegram, "
                             "после чего нажмите /start", parse_mode="Markdown")
        return

    welcome_message = await message.answer(
        "Привет дорогой друг✋\n"
        "Я виртуальный помощник ресторана \"У камина\"\n\n"
        "Давай познакомимся поближе🤗")

    await state.update_data(welcome_message_id=welcome_message.message_id)
    await state.set_state(InitialRegistration.choosing_gender)
    await message.answer("Кто Вы?", reply_markup=kb.kb_gender)



# Обработчик выбора пола
@router.callback_query(F.data.in_(['gender_male', 'gender_female']),
                       InitialRegistration.choosing_gender)
async def gender_choice(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    welcome_message_id = data.get("welcome_message_id")

    if welcome_message_id:
        try:
            # Удаляем приветственное сообщение
            await callback.message.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=welcome_message_id
            )
        except Exception as e:
            print(f"Ошибка удаления сообщения: {e}")

    await state.set_state(InitialRegistration.choosing_profession)  # Переход в следующее состояние
    await callback.message.edit_text("Здорово! 😃 \n\nРасскажи, чем ты занимаешься?",
                                     reply_markup=kb.kb_profession)
    await callback.answer()


# Обработчик выбора профессии
@router.callback_query(F.data.in_(['profession_student', 'profession_business',
                                   'profession_employed', 'profession_freelancer']),
                       InitialRegistration.choosing_profession)
async def profession_choice(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(InitialRegistration.completed_registration)
    await callback.message.edit_text("Отлично! 👍 \nДля получения скидки 10% остался "
                                     "лишь один шаг.\nПерейди в меню и оформи карту "
                                     "лояльности 💳")
    await callback.message.answer("Если кнопки скрыты, то нажми на иконку 🎛 "
                                  "в правом нижнем углу рядом с микрофоном 👌",
                                  reply_markup=kb.main)
    await callback.answer()


# Обработчик кнопки '🍽️ У камина'
@router.message(F.text == '🍽️  У камина')
async def restaurant_description(message: Message):
    link = "https://telegra.ph/MYZHENATY-03-11-2"
    await message.answer(link, parse_mode='Markdown', reply_markup=kb.main)


# Обработчик кнопки '📋️ Меню'
@router.message(F.text == '📋️  Меню')
async def show_menu_options(message: Message):
    await message.answer("Выберите нужное вам меню👇",
                         reply_markup=kb.menu_options_keyboard)


# Обработчик кнопки '🍽️ Основное меню'
@router.message(F.text == '🍽️ Основное меню')
async def send_main_menu_pdf(message: types.Message):
    file_path = 'docs/Main_menu.pdf'
    pdf = FSInputFile(path=file_path, filename='Main_menu.pdf')
    await message.answer_document(document=pdf, caption="Основное меню центрального зала")


# Обработчик кнопки '👶 Детское меню'
@router.message(F.text == '👶 Детское меню')
async def show_menu_kids(message: Message):
    link = "https://disk.yandex.ru/i/Qat0Y1HO88Arvw"
    await message.answer(link, parse_mode='Markdown', reply_markup=kb.menu_options_keyboard)


# Обработчик кнопки '⬅️ Назад'
@router.message(F.text == '⬅️ Назад')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите нужное вам действие👇", reply_markup=kb.main)

