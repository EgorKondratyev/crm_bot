import time

from aiogram.types import Message

from src.core.bot.bot import dp
from src.dao.user import UserDAO


async def start_handler(message: Message):
    await message.answer(determine_time_of_day())
    user = await UserDAO.get_by_telegram_id(telegram_id=message.from_user.id)


def determine_time_of_day():
    time_of_day = time.localtime()
    if time_of_day.tm_hour >= 18:
        return "🌚"
    elif time_of_day.tm_hour <= 3:
        return "🌚"
    else:
        return "🌝"


def register_start_command_handlers():
    dp.register_message_handler(start_handler, content_types="any", commands="start")
