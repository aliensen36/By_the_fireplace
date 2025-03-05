from aiogram import F, Router
from aiogram.types import (CallbackQuery, Message)
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.fsm_states import Registration
from app.handlers.start_handler import start_router
from aiogram.fsm.state import default_state
import app.keyboards.inline as inline_kb
import app.keyboards.reply as reply_kb
from app.text import *

survey_router = Router()

# Обработчик начала анкетирования
@survey_router.message(F.text == '📝 Заполнить анкету')
async def survey_start(message: Message, state: FSMContext):
    await message.answer(survey_message, reply_markup=reply_kb.cancel_keyboard)
    await message.answer("1. Сколько вам лет?",
                         reply_markup=inline_kb.kb_age)
    await state.set_state(Registration.age_group)


# Обработчик выбора возраста
@survey_router.callback_query(Registration.age_group,
                              F.data.in_(['age_18_24', 'age_25_27', 'age_28_40',
                                          'age_41_55', 'age_55_plus']))
async def survey_age_group(callback: CallbackQuery, state: FSMContext):
    await state.update_data(age_group=callback.data)
    await callback.answer()
    await callback.message.edit_text("2. Где вы живете?",
                                  reply_markup=inline_kb.kb_residence)
    await state.set_state(Registration.residence)


# Обработчик выбора места жительства
@survey_router.callback_query(Registration.residence,
                              F.data.in_(['city', 'region', 'tourist']))
async def survey_residence(callback: CallbackQuery, state: FSMContext):
    await state.update_data(residence=callback.data)
    await callback.answer()
    await callback.message.edit_text("3. С кем вы чаще всего посещаете рестораны?",
                                     reply_markup=inline_kb.kb_company)
    await state.set_state(Registration.company)


# Обработчик выбора компании
@survey_router.callback_query(Registration.company,
                              F.data.in_(['alone', 'couple', 'married',
                                          'family', 'friends', 'colleagues']))
async def survey_company(callback: CallbackQuery, state: FSMContext):
    await state.update_data(company=callback.data)
    await callback.answer()
    await callback.message.edit_text("4. Что для вас главное при выборе ресторана?\n\n"
                                     "P.S. Выберите 1 вариант из предложенных или "
                                     "напишите несколько вариантов текстом!",
                                     reply_markup=inline_kb.kb_reason)
    await state.set_state(Registration.reason)


# Обработчик выбора причины
@survey_router.callback_query(Registration.reason,
                              F.data.in_(['quality', 'atmosphere', 'prices',
                                          'location', 'instagrammable',
                                          'service_speed', 'friends_recommend',
                                          'special_offers']))
async def survey_reason(callback: CallbackQuery, state: FSMContext):
    await state.update_data(reason=callback.data)
    await callback.answer()
    await callback.message.edit_text("5. Как вы узнали о нашем ресторане?",
                                     reply_markup=inline_kb.kb_advertising_sources)
    await state.set_state(Registration.advertising_sources)


# Обработчик текстового ответа на вопрос 4
@survey_router.message(Registration.reason)
async def survey_reason_text(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    await message.answer("Спасибо! Ваш ответ записан. ✅")
    await message.answer("5. Как вы узнали о нашем ресторане?",
                         reply_markup=inline_kb.kb_advertising_sources)
    await state.set_state(Registration.advertising_sources)


# Обработчик выбора источника
@survey_router.callback_query(Registration.advertising_sources,
                              F.data.in_(['instagram', 'vk', 'friends_recommend',
                                          'search', 'walk_by']))
async def survey_advertising_sources(callback: CallbackQuery, state: FSMContext):
    await state.update_data(advertising_sources=callback.data)
    await callback.answer()
    await callback.message.edit_text("6. Как часто вы посещаете наш ресторан?",
                                     reply_markup=inline_kb.kb_visit_frequency)
    await state.set_state(Registration.visit_frequency)


# Обработчик выбора частоты посещения
@survey_router.callback_query(Registration.visit_frequency,
                              F.data.in_(['first_time', 'more_than_weekly',
                                          'monthly', 'every_few_months', 'rarely']))
async def survey_visit_frequency(callback: CallbackQuery, state: FSMContext):
    await state.update_data(visit_frequency=callback.data)
    await callback.answer()
    await callback.message.edit_text("7. По какому поводу вы обычно ходите в ресторан",
                                     reply_markup=inline_kb.kb_purpose)
    await state.set_state(Registration.purpose)


# Обработчик выбора повода
@survey_router.callback_query(Registration.purpose,
                              F.data.in_(['everyday_meal', 'date', 'business_meeting',
                                          'family_celebration']))
async def survey_purpose(callback: CallbackQuery, state: FSMContext):
    await state.update_data(purpose=callback.data)
    await callback.answer()
    await callback.message.edit_text("8. Какие блюда и напитки вы заказываете "
                                     "чаще всего?\n\nP.S. Выберите 1 вариант "
                                     "из предложенных или напишите несколько "
                                     "вариантов текстом.",
                                     reply_markup=inline_kb.kb_food_preferences)
    await state.set_state(Registration.food_preferences)


# Обработчик выбора предпочтений
@survey_router.callback_query(Registration.food_preferences,
                              F.data.in_(['meat_dishes', 'fish_seafood', 'vegan_options',
                                          'desserts', 'alcohol_cocktails', 'coffee_tea']))
async def survey_food_preferences(callback: CallbackQuery, state: FSMContext):
    await state.update_data(food_preferences=callback.data)
    await callback.answer()
    await callback.message.edit_text("9. Какие блюда вы бы хотели видеть в нашем меню?\n\n"
                                     "Напишите текстом или пропустите этот вопрос.",
                                     reply_markup=inline_kb.kb_skip)
    await state.set_state(Registration.suggestions)


# Обработчик для предложений блюд
@survey_router.callback_query(Registration.suggestions)
async def survey_suggestions(callback: CallbackQuery, state: FSMContext):
    await state.update_data(suggestions=callback.data)
    await callback.answer()
    await callback.message.edit_text("10. Как бы вы описали атмосферу "
                                     "в нашем ресторане?",
                                     reply_markup=inline_kb.kb_atmosphere)
    await state.set_state(Registration.atmosphere)


# Обработчик текстового ответа на вопрос 9
@survey_router.message(Registration.suggestions)
async def survey_suggestions_text(message: Message, state: FSMContext):
    await state.update_data(suggestions=message.text)
    await message.answer("Спасибо! Ваш ответ записан. ✅")
    await message.answer("10. Как бы вы описали атмосферу"
                         "в нашем ресторане?",
                         reply_markup=inline_kb.kb_atmosphere)
    await state.set_state(Registration.atmosphere)



# Обработчик кнопки 'Отмена'
@survey_router.message(F.text == 'Отмена')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите 👇",
                         reply_markup=reply_kb.main)

