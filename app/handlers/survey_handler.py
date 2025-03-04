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
                                          'special_offers',]))
async def survey_company(callback: CallbackQuery, state: FSMContext):
    await state.update_data(reason=callback.data)
    await callback.answer()
    await callback.message.edit_text("5. Как вы узнали о нашем ресторане?",
                                     reply_markup=inline_kb.kb_advertising_sources)
    await state.set_state(Registration.advertising_sources)


# Обработчик выбора источника
@survey_router.callback_query(Registration.advertising_sources,
                              F.data.in_(['instagram', 'vk', 'friends_recommend',
                                          'search', 'walk_by']))
async def survey_company(callback: CallbackQuery, state: FSMContext):
    await state.update_data(advertising_sources=callback.data)
    await callback.answer()
    await callback.message.edit_text("6. Как часто вы посещаете наш ресторан?",
                                     reply_markup=inline_kb.kb_advertising_sources)
    await state.set_state(Registration.advertising_sources)


# Обработчик кнопки 'Отмена'
@survey_router.message(F.text == 'Отмена')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите 👇",
                         reply_markup=reply_kb.main)

