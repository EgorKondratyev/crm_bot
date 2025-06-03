from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from src.core.bot.bot import dp
from src.core.database.models import Cargo
from src.dao.cargo import CargoDAO
from src.dao.user import UserDAO
from src.keyboards.inline.cargo import create_keyboard_cargos


async def get_client_cargos_handler(message: Message):
    user = await UserDAO.get_by_telegram_id(telegram_id=message.from_user.id)
    await message.answer(
        "<b>Выберите заказ:</b> ",
        reply_markup=create_keyboard_cargos(cargos=user.cargos),
        parse_mode="html",
    )


async def get_client_cargo_handler(callback: CallbackQuery):
    await callback.answer("Ищем заказ...")
    cargo: Cargo = await CargoDAO.find_one_or_none(
        model_id=int(callback.data.split(":")[1])
    )
    await callback.message.answer(
        f"<b>Информация по заказу #{cargo.id}</b>\n\n"
        f"<b>Дата оформления заказа:</b> {cargo.created_at}\n\n"
        f"<b>Текущий статус:</b> {cargo.status.value}\n\n"
        f"<b>Тип перевозки:</b> {cargo.shipping.value}\n\n"
        f"<b>Тип транспорта:</b> {cargo.transport.value}\n\n"
        f"<b>Вес/Ширина/Высота:</b> {cargo.weight}/{cargo.width}/{cargo.height}\n\n"
        f"<b>Место отправки груза:</b> {cargo.shipping_address}\n\n"
        f"<b>Место назначения груза:</b> {cargo.destination_address}",
        parse_mode="html",
    )


def register_cargo_handlers():
    dp.register_message_handler(get_client_cargos_handler, Text(equals="🚛 Мои заказы"))
    dp.register_callback_query_handler(
        get_client_cargo_handler, Text(startswith="get_cargo:")
    )
