import asyncio
from aiogram import Bot, Dispatcher

from src.core.config import config
from src.core.database import Database
from src.core.storage import memory

bot = Bot(token=config.bot.token)
main_loop = asyncio.get_event_loop()
dp = Dispatcher(bot=bot, storage=memory, loop=main_loop)
db = Database()  # without punq
