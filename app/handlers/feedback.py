from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram import F, Router
import app.keyboards.reply as reply_kb
from app.fsm_states import FeedbackState
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Feedback

feedback_router = Router()


# Обработчик кнопки '📝️ Оставить отзыв'
@feedback_router.message(F.text == '📝 Оставить отзыв')
async def feedback_menu(message: Message):
    await message.answer('Выбери, пожалуйста, вариант обратной связи👇',
                         reply_markup=reply_kb.kb_feedback)


# Обработчик кнопки '💬 Оставить отзыв'
@feedback_router.message(F.text == '💬 Оставить отзыв')
async def write_feedback(message: Message, state: FSMContext):
    await message.answer('Мы всегда рады любым честным отзывам, так как вы '
                         'помогаете нам повышать уровень сервиса и качество '
                         'обслуживания.\n\nНапишите отзыв и отправьте его в чат 🔽',
                         reply_markup=reply_kb.cancel_keyboard)
    await state.set_state(FeedbackState.text_to_chat)


@feedback_router.message(FeedbackState.text_to_chat)
async def receive_feedback_text(message: Message, state: FSMContext,
                                session: AsyncSession):
    await state.update_data(text_to_chat=message.text)

    text_to_chat = message.text
    tg_id = message.from_user.id

    feedback = Feedback(tg_id=tg_id, text_to_chat=text_to_chat)
    session.add(feedback)
    await session.commit()
    await message.answer('Спасибо за ваш отзыв! ❤️',
                         reply_markup=reply_kb.main)

    # Отправка отзыва в группу админов
    bot = message.bot
    try:
        await bot.send_message(
            chat_id=-1002551570110,
            text=f'📬 Новый отзыв от @{message.from_user.username or tg_id}:\n\n{text_to_chat}'
        )
    except Exception as e:
        print(f'Не удалось отправить отзыв в чат: {e}')

    await state.clear()



# Обработчик кнопки '✉️ Написать директору'
@feedback_router.message(F.text == '✉️ Написать директору')
async def feedback_to_boss(message: Message, state: FSMContext):
    await message.answer('📝 Оцените нас от 1 до 10 баллов или напишите '
                         'Свой отзыв и он прямиком улетит владельцу заведения.',
                         reply_markup=reply_kb.cancel_keyboard)
    await state.set_state(FeedbackState.text_to_boss)


@feedback_router.message(FeedbackState.text_to_boss)
async def feedback_to_boss(message: Message, state: FSMContext,
                           session: AsyncSession):
    await state.update_data(text_to_boss=message.text)
    text_to_boss = message.text
    tg_id = message.from_user.id

    feedback = Feedback(tg_id=tg_id, text_to_boss=text_to_boss)
    session.add(feedback)
    await session.commit()
    await message.answer('Спасибо за ваш отзыв! ❤️',
                         reply_markup=reply_kb.main)

    # Отправка отзыва директору
    bot = message.bot
    try:
        await bot.send_message(chat_id=-1002551570110,
                               text="‼️‼️ <b>Сообщение для директора</b> ‼️‼️\n"
                                    "@KateAlexandrova\n\n"
                                    f"📬 Новый отзыв от @{message.from_user.username 
                                                         or tg_id}:\n\n"
                                    f"{text_to_boss}",
                               parse_mode="HTML")
    except Exception as e:
        print(f'Не удалось отправить отзыв директору: {e}')

    await state.clear()