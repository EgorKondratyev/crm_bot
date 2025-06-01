from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from src.core.bot.bot import dp


async def stop_fsm_handler(message: [Message, CallbackQuery], state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        try:  # callback
            await message.answer()
            await message.message.answer("Нет запущенных процессов")
        except Exception:  # message
            await message.answer("Нет запущенных процессов")
        return

    await state.finish()
    try:
        await message.answer()
        await message.message.edit_text(
            "Операция успешно остановлена!", parse_mode="html"
        )
    except Exception:  # message
        await message.answer(f"Операция успешно остановлена!")


def register_stop_fsm_handler():
    dp.register_message_handler(
        stop_fsm_handler, commands=["stop", "cancel"], state="*"
    )
    dp.register_message_handler(
        stop_fsm_handler,
        Text(equals=["stop", "Остановить❌"], ignore_case=True),
        state="*",
    )
    dp.register_callback_query_handler(
        stop_fsm_handler,
        Text(equals="stop_fsm", ignore_case=True),
        state="*",
    )
