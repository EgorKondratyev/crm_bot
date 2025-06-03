from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from src.core.bot.bot import dp


async def get_personal_area_handler(message: Message):
    pass


def register_personal_area_handlers():
    dp.register_message_handler(
        get_personal_area_handler, Text(equals="🔒 Личный кабинет")
    )
