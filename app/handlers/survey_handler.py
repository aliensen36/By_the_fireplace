from aiogram import F, Router
from aiogram.types import (CallbackQuery, Message)
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.fsm_states import Registration
from app.handlers.start_handler import start_router
import app.keyboards.inline as inline_kb

router = Router()

# Обработчик анкетирования '📝 Заполнить анкету'
@start_router.callback_query(StateFilter(Registration.age_group), F.text == '📝  Заполнить анкету')
async def survey(callback: CallbackQuery, state: FSMContext):
    await callback.answer(
        "Мы очень рады, что вы выбрали наш ресторан!\n"
        "Нам важно, чтобы каждый гость чувствовал себя здесь по-настоящему особенным. "
        "Помогите нам стать лучше — ответьте на несколько коротких вопросов.\n"
        "Это займет не больше 10 минут, а ваше мнение станет ценным вкладом в улучшение нашего сервиса, меню и атмосферы.\n"
        "Заранее спасибо за вашу искренность!\n\n"
        "А в конце вас ждет приятный подарок 😉"
    )

    data = await state.get_data()
    welcome_message_id = data.get("welcome_message_id")

    if welcome_message_id:
        try:
            # Удаление приветственного сообщения
            await callback.message.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=welcome_message_id
            )
        except Exception as e:
            print(f"Ошибка удаления сообщения: {e}")

    await state.update_data(gender=callback.data)
    await state.set_state(Registration.profession)
    await callback.message.edit_text("Здорово! 😃 \n\nРасскажи, чем ты занимаешься?",
                                     reply_markup=inline_kb.kb_age)
    await callback.answer()
