from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from src.core.bot.bot import dp
from src.dao.user import UserDAO
from src.keyboards.inline.personal_area import create_keyboard_personal_area


async def get_personal_area_handler(message: Message):
    user = await UserDAO.get_by_telegram_id(telegram_id=message.from_user.id)
    if not user:
        await message.answer(
            "Вы не зарегистрированы в системе для просмотра личного кабинета!"
        )
        return
    
    await message.answer(
        f"<b>Добро пожаловать в личный кабинет</b> 🛠\n\n"
        f"<b>Ваш ID в телеграм:</b> {user.telegram_id}\n\n"
        f"<b>Номер телефона:</b> {user.phone_number}\n\n"
        f"<b>Бизнес модель:</b> {user.business_type.value}\n\n"
        f"<b>Количество заказов в системе:</b> {len(user.cargos)}",
        parse_mode="html",
        reply_markup=create_keyboard_personal_area(),
    )


def register_personal_area_handlers():
    dp.register_message_handler(
        get_personal_area_handler, Text(equals="🔒 Личный кабинет")
    )
