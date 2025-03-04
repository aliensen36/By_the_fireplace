from aiogram import F, Router
from aiogram.types import (CallbackQuery, Message)
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.fsm_states import Registration
from app.handlers.start_handler import start_router
from aiogram.fsm.state import default_state
import app.keyboards.inline as inline_kb
from app.text import *

survey_router = Router()

# Обработчик анкетирования '📝 Заполнить анкету'
@survey_router.message(F.text == '📝 Заполнить анкету')
async def survey_start(message: Message, state: FSMContext):
    await message.answer(survey_message)
    await state.set_state(Registration.age_group)
    await message.answer("1. Сколько вам лет?",
                         reply_markup=inline_kb.kb_age)


# @survey_router.callback_query(StateFilter(default_state), F.data.in_(['age_18_24',
#                                                                'age_25_27',
#                                                                'age_28_40',
#                                                                'age_41_55',
#                                                                'age_55_plus']))
# async def survey(callback: CallbackQuery, ):