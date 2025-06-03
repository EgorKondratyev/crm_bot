from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.database.models.cargo import ShippingType, TransportType


def get_shipping_type_buttons():
    menu = InlineKeyboardMarkup(row_width=2)
    for shipping in ShippingType:
        button = InlineKeyboardButton(
            text=shipping.value, callback_data=f"order_shipping:{shipping.name}"
        )
        menu.insert(button)
    return menu


def get_transport_type_buttons():
    menu = InlineKeyboardMarkup(row_width=1)
    for transport in TransportType:
        button = InlineKeyboardButton(
            text=transport.value, callback_data=f"order_transport:{transport.name}"
        )
        menu.insert(button)
    return menu
