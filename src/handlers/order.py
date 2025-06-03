from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from src.core.bot.bot import dp
from src.core.database.models.cargo import ShippingType, TransportType
from src.dao.cargo import CargoDAO
from src.dao.user import UserDAO
from src.keyboards.inline.order import (
    get_shipping_type_buttons,
    get_transport_type_buttons,
)
from src.keyboards.markup import get_main_buttons_for_client
from src.states.order import PlacingOrderFSM


async def placing_order_choice_shipping_handler(message: Message):
    await PlacingOrderFSM.get_shipping.set()
    await message.answer(
        "Выберите тип перевозки", reply_markup=get_shipping_type_buttons()
    )


async def placing_order_choice_transport_handler(
    callback: CallbackQuery, state: FSMContext
):
    shipping_type = callback.data.split(":")[1]
    async with state.proxy() as data:
        data["shipping_type"] = shipping_type
    await callback.answer("Тип перевозки успешно выбран")
    await callback.message.answer(
        f"Выбранный тип перевозки: <b>{ShippingType.get_by_key(key=shipping_type)}</b>",
        parse_mode="html",
    )

    await PlacingOrderFSM.get_transport.set()
    await callback.message.answer(
        "Выберите нужный вид транспорта", reply_markup=get_transport_type_buttons()
    )


async def placing_order_input_weight_handler(
    callback: CallbackQuery, state: FSMContext
):
    transport_type = callback.data.split(":")[1]
    async with state.proxy() as data:
        data["transport_type"] = transport_type
        shipping_type = data["shipping_type"]
    await callback.answer("Тип транспорта успешно выбран")
    await callback.message.answer(
        f"Выбранный тип транспорта: <b>{TransportType.get_by_key(key=transport_type)}</b>",
        parse_mode="html",
    )

    await PlacingOrderFSM.get_weight.set()
    if shipping_type == "PASSENGER":
        await callback.message.answer("Напишите количество людей:")
    else:
        await callback.message.answer("Напишите вес груза в кг:")


async def placing_order_input_width_handler(message: Message, state: FSMContext):
    try:
        weight = int(message.text)
    except Exception as e:
        await message.answer("Вес должен быть целочисленным\n\nНапишите вес груза:")
        return
    if weight > 10000:
        await message.answer("Вес не должен превышать 10000кг\n\nНапишите вес груза:")
        return
    async with state.proxy() as data:
        data["weight"] = weight

    await PlacingOrderFSM.get_width.set()
    await message.answer(
        "<b>Напишите ширину груза в метрах:</b>\n\n"
        "*Необязательный параметр. Введите <code>0</code>, чтобы пропустить.",
        parse_mode="html",
    )


async def placing_order_input_height_handler(message: Message, state: FSMContext):
    try:
        width = int(message.text)
    except Exception as e:
        await message.answer(
            "Ширина должна быть целочисленным числом\n\nНапишите ширину груза:"
        )
        return
    async with state.proxy() as data:
        data["width"] = width

    await PlacingOrderFSM.get_height.set()
    await message.answer(
        "<b>Напишите высоту груза в метрах:</b>\n\n"
        "*Необязательный параметр. Введите <code>0</code>, чтобы пропустить.",
        parse_mode="html",
    )


async def placing_order_input_destination_address_handler(
    message: Message, state: FSMContext
):
    try:
        height = int(message.text)
    except Exception as e:
        await message.answer(
            "Высота должна быть целочисленным числом\n\nНапишите высоту груза:"
        )
        return
    async with state.proxy() as data:
        data["height"] = height

    await PlacingOrderFSM.get_destination_address.set()
    await message.answer(
        "<b>Напишите место назначения груза: </b>\n\n"
        "<i>Пример:</i> *190000, Россия, г. Санкт-Петербург, Центральный р-н, Невский пр-т, д. 100, лит. А, оф. 305*\n",
        parse_mode="html",
    )


async def placing_order_input_shipping_address_handler(
    message: Message, state: FSMContext
):
    destination_address = message.text
    if len(destination_address) >= 500:
        await message.answer(
            "Место назначения груза не может превышать более 500 символов!\n\n"
            "<b>Напишите место назначения груза: </b>",
            parse_mode="html",
        )
        return
    async with state.proxy() as data:
        data["destination_address"] = destination_address

    await PlacingOrderFSM.get_shipping_address.set()
    await message.answer(
        "<b>Напишите место отправки груза: </b>\n\n",
        parse_mode="html",
    )


async def placing_order_finished_handler(message: Message, state: FSMContext):
    shipping_address = message.text
    if len(shipping_address) >= 500:
        await message.answer(
            "Место назначения отправки не может превышать более 500 символов!\n\n"
            "<b>Напишите место назначения груза: </b>",
            parse_mode="html",
        )
        return

    async with state.proxy() as data:
        destination_address = data["destination_address"]
        height = data["height"]
        width = data["width"]
        weight = data["weight"]
        transport_type = data["transport_type"]
        shipping_type = data["shipping_type"]
    await state.finish()

    user = await UserDAO.get_by_telegram_id(telegram_id=message.from_user.id)
    await CargoDAO.add(
        shipping_address=shipping_address,
        destination_address=destination_address,
        height=height,
        width=width,
        weight=weight,
        transport=transport_type,
        shipping=shipping_type,
        user_id=user.id,
    )

    await message.answer(
        "Заявка успешно создана🚚✨! "
        "Ожидайте, скоро с Вами свяжется наш специалист для уточнения дополнительных деталей заказа."
    )
    await message.answer(
        "«Отслеживайте доставку в реальном времени в разделе «Мои заказы».",
        reply_markup=get_main_buttons_for_client(),
    )


def register_order_handlers():
    dp.register_message_handler(
        placing_order_choice_shipping_handler,
        Text(equals="✅ Оформить доставку"),
    )
    dp.register_callback_query_handler(
        placing_order_choice_transport_handler,
        Text(startswith="order_shipping:"),
        state=PlacingOrderFSM.get_shipping,
    )
    dp.register_callback_query_handler(
        placing_order_input_weight_handler,
        Text(startswith="order_transport:"),
        state=PlacingOrderFSM.get_transport,
    )
    dp.register_message_handler(
        placing_order_input_width_handler,
        state=PlacingOrderFSM.get_weight,
    )
    dp.register_message_handler(
        placing_order_input_height_handler,
        state=PlacingOrderFSM.get_width,
    )
    dp.register_message_handler(
        placing_order_input_destination_address_handler,
        state=PlacingOrderFSM.get_height,
    )
    dp.register_message_handler(
        placing_order_input_shipping_address_handler,
        state=PlacingOrderFSM.get_destination_address,
    )
    dp.register_message_handler(
        placing_order_finished_handler,
        state=PlacingOrderFSM.get_shipping_address,
    )
