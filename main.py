import logging

from aiogram import executor

from src.core.bot.bot import dp
from src.core.bot.command import set_commands

logger = logging.getLogger(__name__)


async def start(_):
    await set_commands()
    logger.debug('Бот успешно запущен!')


async def end(_):
    logger.debug('Бот успешно отключен!')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=start, on_shutdown=end)
