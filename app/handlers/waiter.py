from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F, Router
import app.keyboards.reply as reply_kb
from app.fsm_states import CallWaiterState

waiter_router = Router()


# Обработчик кнопки '🛎️ Вызов официанта'
@waiter_router.message(F.text == '🛎️ Вызов официанта')
async def call_waiter(message: Message, state: FSMContext):
    await message.answer('Введите номер столика и комментарий для официанта, '
                         '(например, стол 1, принесите счёт).',
                         reply_markup=reply_kb.cancel_keyboard)
    await state.set_state(CallWaiterState.call_waiter)


@waiter_router.message(CallWaiterState.call_waiter)
async def receive_call_waiter_text(message: Message, state: FSMContext):
    await state.update_data(call_waiter=message.text)
    cw_text = message.text
    tg_id = message.from_user.id
    username = message.from_user.username or tg_id

    # Отправка вызова в группу админов
    bot = message.bot
    try:
        await bot.send_message(chat_id=-1002638197567,
                               text=f"🛎️🛎️ <b>Вызов официанта</b> 🛎️🛎️\n\n"
                                    f"👤 Клиент @{username}:\n\n"
                                    f"{cw_text}",
                               parse_mode="HTML")
    except Exception as e:
            print(f'Не удалось отправить вызов в чат: {e}')
    await state.clear()

    # Ответ пользователю
    await message.answer("🕐 Официант уже спешит к вам! 😊",
                         reply_markup=reply_kb.main)


# Обработчик кнопки 'Отмена'
@waiter_router.message(F.text == 'Отмена')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите 👇",
                         reply_markup=reply_kb.main)
