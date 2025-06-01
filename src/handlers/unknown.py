from aiogram.types import Message

from src.core.bot.bot import dp


async def unknown_command_handler(message: Message):
    await message.answer(
        "Приносим наши извинения, система не смогла распознать Ваш запрос, "
        "повторите его или обратитесь в тех. поддержку /help",
        parse_mode="html",
    )


def register_unknown_command_handlers():
    dp.register_message_handler(unknown_command_handler)
