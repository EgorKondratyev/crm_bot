import time

from aiogram.types import Message

from src.core.bot.bot import dp
from src.dao.user import UserDAO
from src.keyboards.markup import phone_request_kb, get_main_buttons_for_client
from src.states.register import RegisterFSM


async def start_handler(message: Message):
    await message.answer(determine_time_of_day())
    user = await UserDAO.get_by_telegram_id(telegram_id=message.from_user.id)
    if user:
        await message.answer(
            "Приветствуем в компании <b>«Метеор»!</b> 🌤️\n\n"
            "<b>Поддержка</b> → если возникли трудности или неполадки.\n\n"
            "<b>Личный кабинет</b> → подробная/личная информация о Вашем аккаунте.\n\n"
            "<b>Мои заказы</b> → все оформленные заказы в нашем приложении",
            reply_markup=get_main_buttons_for_client(),
            parse_mode="html",
        )
    else:
        await RegisterFSM.get_phone.set()
        await message.answer(
            "Приветствуем! 🌤️\n\n"
            "Рады видеть вас в компании <b>«Метеор»!</b> "
            "Чтобы продолжить работу и обеспечить вам максимально удобное обслуживание, пожалуйста, "
            "<b>укажите ваш номер телефона</b> по кнопке ниже 👇",
            parse_mode="html",
            reply_markup=phone_request_kb,
        )
        await message.answer(
            "Обращаем Ваше внимание, что при регистрации на нашем сервисе Вы автоматически соглашаетесь "
            "на обработку персональных данных"
        )


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
