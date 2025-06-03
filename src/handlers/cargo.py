from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from src.core.bot.bot import dp


async def get_client_cargo_handler(message: Message):
    pass


def register_cargo_handlers():
    dp.register_message_handler(get_client_cargo_handler, Text(equals="🚛 Мои заказы"))
