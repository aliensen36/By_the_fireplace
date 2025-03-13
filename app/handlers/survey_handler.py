from aiogram import F, Router
from aiogram.types import (CallbackQuery, Message)
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.fsm_states import *
from app.handlers.start_handler import start_router
from aiogram.fsm.state import default_state
import app.keyboards.inline as inline_kb
import app.keyboards.reply as reply_kb
from app.text import *
from database.orm_query import orm_survey

survey_router = Router()

# Обработчик начала анкетирования
@survey_router.message(F.text == '📝 Заполнить анкету')
async def survey_start(message: Message, state: FSMContext):
    await message.answer(survey_start_message, reply_markup=reply_kb.cancel_keyboard)
    await message.answer("1. Сколько вам лет?",
                         reply_markup=inline_kb.kb_age)
    await state.set_state(Survey.age_group)


# Обработчик выбора возраста (вопрос 1)
@survey_router.callback_query(Survey.age_group,
                              F.data.in_(['age_18_24', 'age_25_27', 'age_28_40',
                                          'age_41_55', 'age_55_plus']))
async def survey_age_group(callback: CallbackQuery, state: FSMContext):
    await state.update_data(age_group=callback.data)
    await callback.answer()
    await callback.message.edit_text("2. Где вы живете?",
                                  reply_markup=inline_kb.kb_residence)
    await state.set_state(Survey.residence)


# Обработчик выбора места жительства (вопрос 2)
@survey_router.callback_query(Survey.residence,
                              F.data.in_(['city', 'region', 'tourist']))
async def survey_residence(callback: CallbackQuery, state: FSMContext):
    await state.update_data(residence=callback.data)
    await callback.answer()
    await callback.message.edit_text("3. С кем вы чаще всего посещаете рестораны?",
                                     reply_markup=inline_kb.kb_company)
    await state.set_state(Survey.company)


# Обработчик выбора компании (вопрос 3)
@survey_router.callback_query(Survey.company,
                              F.data.in_(['alone', 'couple', 'married',
                                          'family', 'friends', 'colleagues']))
async def survey_company(callback: CallbackQuery, state: FSMContext):
    await state.update_data(company=callback.data)
    await callback.answer()
    await callback.message.edit_text("4. Что для вас главное при выборе ресторана?\n\n"
                                     "P.S. Выберите 1 вариант из предложенных или "
                                     "напишите несколько вариантов текстом!",
                                     reply_markup=inline_kb.kb_reason)
    await state.set_state(Survey.reason)


# Обработчик выбора причины (вопрос 4)
@survey_router.callback_query(Survey.reason,
                              F.data.in_(['quality', 'atmosphere', 'prices',
                                          'location', 'instagrammable',
                                          'service_speed', 'friends_recommend',
                                          'special_offers']))
async def survey_reason(callback: CallbackQuery, state: FSMContext):
    await state.update_data(reason=callback.data)
    await callback.answer()
    await callback.message.edit_text("5. Как вы узнали о нашем ресторане?",
                                     reply_markup=inline_kb.kb_advertising_sources)
    await state.set_state(Survey.advertising_sources)


# Обработчик текстового ответа на вопрос 4
@survey_router.message(Survey.reason)
async def survey_reason_text(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    await message.answer("Спасибо! Ваш ответ записан. ✅")
    await message.answer("5. Как вы узнали о нашем ресторане?",
                         reply_markup=inline_kb.kb_advertising_sources)
    await state.set_state(Survey.advertising_sources)


# Обработчик выбора источника (вопрос 5)
@survey_router.callback_query(Survey.advertising_sources,
                              F.data.in_(['instagram', 'vk', 'friends_recommend',
                                          'search', 'walk_by']))
async def survey_advertising_sources(callback: CallbackQuery, state: FSMContext):
    await state.update_data(advertising_sources=callback.data)
    await callback.answer()
    await callback.message.edit_text("6. Как часто вы посещаете наш ресторан?",
                                     reply_markup=inline_kb.kb_visit_frequency)
    await state.set_state(Survey.visit_frequency)


# Обработчик выбора частоты посещения (вопрос 6)
@survey_router.callback_query(Survey.visit_frequency,
                              F.data.in_(['first_time', 'more_than_weekly',
                                          'monthly', 'every_few_months', 'rarely']))
async def survey_visit_frequency(callback: CallbackQuery, state: FSMContext):
    await state.update_data(visit_frequency=callback.data)
    await callback.answer()
    await callback.message.edit_text("7. По какому поводу вы обычно ходите в ресторан",
                                     reply_markup=inline_kb.kb_purpose)
    await state.set_state(Survey.purpose)


# Обработчик выбора повода (вопрос 7)
@survey_router.callback_query(Survey.purpose,
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
    await state.set_state(Survey.food_preferences)


# Обработчик выбора предпочтений (вопрос 8)
@survey_router.callback_query(Survey.food_preferences,
                              F.data.in_(['meat_dishes', 'fish_seafood', 'vegan_options',
                                          'desserts', 'alcohol_cocktails', 'coffee_tea']))
async def survey_food_preferences(callback: CallbackQuery, state: FSMContext):
    await state.update_data(food_preferences=callback.data)
    await callback.answer()
    await callback.message.edit_text("9. Какие блюда вы бы хотели видеть в нашем меню?\n\n"
                                     "Напишите текстом или пропустите этот вопрос.",
                                     reply_markup=inline_kb.kb_skip)
    await state.set_state(Survey.suggestions)


# Обработчик текстового ответа на вопрос 8
@survey_router.message(Survey.food_preferences)
async def survey_food_preferences_text(message: Message, state: FSMContext):
    await state.update_data(food_preferences=message.text)
    await message.answer("Спасибо! Ваш ответ записан. ✅")
    await message.answer("9. Какие блюда вы бы хотели видеть в нашем меню?\n\n"
                         "Напишите текстом или пропустите этот вопрос.",
                         reply_markup=inline_kb.kb_skip)
    await state.set_state(Survey.suggestions)


# Обработчик для предложений блюд (вопрос 9)
@survey_router.callback_query(Survey.suggestions)
async def survey_suggestions(callback: CallbackQuery, state: FSMContext):
    await state.update_data(suggestions=callback.data)
    await callback.answer()
    await callback.message.edit_text("10. Как бы вы описали атмосферу "
                                     "в нашем ресторане?",
                                     reply_markup=inline_kb.kb_atmosphere)
    await state.set_state(Survey.atmosphere)


# Обработчик текстового ответа на вопрос 9
@survey_router.message(Survey.suggestions)
async def survey_suggestions_text(message: Message, state: FSMContext):
    await state.update_data(suggestions=message.text)
    await message.answer("Спасибо! Ваш ответ записан. ✅")
    await message.answer("10. Как бы вы описали атмосферу"
                         "в нашем ресторане?",
                         reply_markup=inline_kb.kb_atmosphere)
    await state.set_state(Survey.atmosphere)


# Обработчик выбора атмосферы (вопрос 10)
@survey_router.callback_query(Survey.atmosphere,
                              F.data.in_(['cozy_relaxing', 'modern_stylish',
                                          'loud_lively', 'ordinary']))
async def survey_atmosphere(callback: CallbackQuery, state: FSMContext):
    await state.update_data(atmosphere=callback.data)
    await callback.answer()
    await callback.message.edit_text("11. Что вам нравится в обслуживании?",
                                     reply_markup=inline_kb.kb_service_rating)
    await state.set_state(Survey.service_rating)


# Обработчик оценки обслуживания (вопрос 11)
@survey_router.callback_query(Survey.service_rating,
                              F.data.in_(['speed', 'politeness', 'attention_to_details',
                                          'everything_good']))
async def survey_service_rating(callback: CallbackQuery, state: FSMContext):
    await state.update_data(service_rating=callback.data)
    await callback.answer()
    await callback.message.edit_text("12. Что бы вы улучшили в нашем ресторане?\n\n"
                                     "P.S. Выберите 1 вариант из предложенных или "
                                     "напишите несколько вариантов текстом!",
                                     reply_markup=inline_kb.kb_improvements)
    await state.set_state(Survey.improvements)


# Обработчик текстового ответа на вопрос 11
@survey_router.message(Survey.service_rating)
async def survey_service_rating_text(message: Message, state: FSMContext):
    await state.update_data(service_rating=message.text)
    await message.answer("Спасибо! Ваш ответ записан. ✅")
    await message.answer("12. Что бы вы улучшили в нашем ресторане?\n\n"
                         "P.S. Выберите 1 вариант из предложенных или "
                         "напишите несколько вариантов текстом!",
                         reply_markup=inline_kb.kb_improvements)
    await state.set_state(Survey.improvements)


# Обработчик для улучшений (вопрос 12)
@survey_router.callback_query(Survey.improvements,
                              F.data.in_(['update_menu', 'update_interior',
                                          'lower_prices', 'better_music']))
async def survey_improvements(callback: CallbackQuery, state: FSMContext):
    await state.update_data(improvements=callback.data)
    await callback.answer()
    await state.set_state(Survey.obstacles)
    await callback.message.edit_text("13. Что мешает вам посещать нас чаще?",
                                     reply_markup=inline_kb.kb_obstacles)
    await state.set_state(Survey.obstacles)


# Обработчик текстового ответа на вопрос 12
@survey_router.message(Survey.improvements)
async def survey_improvements_text(message: Message, state: FSMContext):
    await state.update_data(improvements=message.text)
    await message.answer("Спасибо! Ваш ответ записан. ✅")
    await message.answer("13. Что мешает вам посещать нас чаще?",
                         reply_markup=inline_kb.kb_obstacles)
    await state.set_state(Survey.obstacles)


# Обработчик для помех (вопрос 13)
@survey_router.callback_query(Survey.obstacles,
                              F.data.in_(['high_prices', 'inconvenient_location',
                                          'limited_menu', 'poor_service', 'no_obstacles']))
async def survey_obstacles(callback: CallbackQuery, state: FSMContext):
    await state.update_data(obstacles=callback.data)
    await callback.answer()
    await state.set_state(Survey.restaurants)
    await callback.message.edit_text("14. Какие рестораны вы чаще всего "
                                     "посещаете (помимо нашего)?",
                                     reply_markup=inline_kb.kb_restaurants)
    await state.set_state(Survey.restaurants)


# Обработчик для типов ресторанов (вопрос 14)
@survey_router.callback_query(Survey.restaurants,
                              F.data.in_(['chain_restaurants', 'fine_dining', 'cafes', 'bars']))
async def survey_restaurants(callback: CallbackQuery, state: FSMContext):
    await state.update_data(restaurants=callback.data)
    await callback.answer()
    await state.set_state(Survey.news)
    await callback.message.edit_text("15. Как вы предпочитаете получать новости ресторана?",
                                     reply_markup=inline_kb.kb_news)
    await state.set_state(Survey.news)


# Обработчик способа получения новостей (вопрос 15)
@survey_router.callback_query(Survey.news,
                              F.data.in_(['news_social', 'news_telegram', 'news_site_app']))
async def survey_news(callback: CallbackQuery, state: FSMContext):
    await state.update_data(news=callback.data)
    await callback.answer()
    await callback.message.edit_text("16. Что бы вы пожелали нашему ресторану? "
                                     "Напишите текстом.",
                                     reply_markup=inline_kb.kb_skip)
    await state.set_state(Survey.wishes)


# Обработчик текстового ответа на вопрос 15
@survey_router.message(Survey.news)
async def survey_news_text(message: Message, state: FSMContext):
    await state.update_data(news=message.text)
    await message.answer("Спасибо! Ваш ответ записан. ✅")
    await message.answer("16. Что бы вы пожелали нашему ресторану? "
                         "Напишите текстом.",
                         reply_markup=inline_kb.kb_skip)
    await state.set_state(Survey.wishes)


# Обработчик для пожеланий (вопрос 16)
@survey_router.callback_query(Survey.wishes)
async def survey_wishes(callback: CallbackQuery, state: FSMContext):
    await state.update_data(wishes=callback.data)
    await callback.answer()
    await callback.message.edit_text("17. Насколько вы готовы рекомендовать "
                                     "нас друзьям по шкале от 1 (не готов) до 10 "
                                     "(обязательно порекомендую)?",
                                     reply_markup=inline_kb.kb_recommendation)
    await state.set_state(Survey.recommendation)


# Обработчик текстового ответа на вопрос 16
@survey_router.message(Survey.wishes)
async def survey_wishes_text(message: Message, state: FSMContext):
    await state.update_data(wishes=message.text)
    await message.answer("Спасибо! Ваш ответ записан. ✅")
    await message.answer("17. Насколько вы готовы рекомендовать "
                         "нас друзьям по шкале от 1 (не готов) до 10 "
                         "(обязательно порекомендую)?",
                         reply_markup=inline_kb.kb_recommendation)
    await state.set_state(Survey.recommendation)


# Обработчик для шкалы рекомендаций (вопрос 17)
@survey_router.callback_query(Survey.recommendation)
async def survey_recommendation(callback: CallbackQuery, state: FSMContext):
    await state.update_data(recommendation=callback.data)
    await callback.answer()
    await callback.message.edit_text("18. И последний вопрос. Почему вы "
                                     "поставили такую оценку? Напишите текстом.",
                                     reply_markup=inline_kb.kb_skip)
    await state.set_state(Survey.explanation)


# Обработчик для пояснения (вопрос 18)
@survey_router.callback_query(Survey.explanation)
async def survey_explanation(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(explanation=callback.data)
    await callback.answer()

    data = await state.get_data()
    await orm_survey(session, user_id=callback.from_user.id, data=data)

    photo_path = 'docs/present.jpg'
    await callback.message.answer_photo(photo=FSInputFile(photo_path),
                                        caption=survey_finish_message)
    await callback.message.answer('Выберите действие 👇',
                                  reply_markup=reply_kb.get_keyboard(
                                      '🍽️ У камина', '📋️ Меню',
                                      '📅🍽️ Забронировать стол', '🚚️ Доставка',
                                      '📍 Путь к нам', '🎁 Программа лояльности',
                                      '📝️ Оставить отзыв', '🛎️  Вызов официанта',
                                      '📝 Заполнить анкету',
                                      placeholder="Что вас интересует?",
                                      sizes=(2, 1, 2, 1, 2, 1),
                                  ))

    await state.clear()


# Обработчик текстового ответа на вопрос 18
@survey_router.message(Survey.explanation)
async def survey_explanation_text(message: Message, state: FSMContext,
                                  session: AsyncSession):
    await state.update_data(explanation=message.text)
    await message.answer("Спасибо! Ваш ответ записан. ✅")

    data = await state.get_data()
    await orm_survey(session, user_id=message.from_user.id, data=data)

    photo_path = 'docs/present.jpg'
    await message.answer_photo(photo=FSInputFile(photo_path),
                               caption=survey_finish_message)
    await message.answer('Выберите действие 👇',
                         reply_markup=reply_kb.get_keyboard(
                             '🍽️ У камина', '📋️ Меню',
                             '📅🍽️ Забронировать стол', '🚚️ Доставка',
                             '📍 Путь к нам', '🎁 Программа лояльности',
                             '📝️ Оставить отзыв', '🛎️  Вызов официанта',
                             '📝 Заполнить анкету',
                             placeholder="Что вас интересует?",
                             sizes=(2, 1, 2, 1, 2, 1),
                         ))
    await state.clear()


# Обработчик кнопки 'Отмена'
@survey_router.message(F.text == 'Отмена')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите 👇",
                         reply_markup=reply_kb.get_keyboard(
                             '🍽️ У камина', '📋️ Меню', '📅🍽️ Забронировать стол',
                             '🚚️ Доставка', '📍 Путь к нам', '🎁 Программа лояльности',
                             '📝️ Оставить отзыв', '🛎️  Вызов официанта', '📝 Заполнить анкету',
                             placeholder="Что вас интересует?",
                             sizes=(2, 1, 2, 1, 2, 1),
                         ))

