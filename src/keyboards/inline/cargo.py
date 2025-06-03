from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.database.models import Cargo


def create_keyboard_cargos(cargos: list[Cargo]) -> InlineKeyboardMarkup:
    menu = InlineKeyboardMarkup(row_width=1)
    for cargo in cargos:
        cargo_button = InlineKeyboardButton(
            f"Заказ #{cargo.id}", callback_data=f"get_cargo:{cargo.id}"
        )
        menu.insert(cargo_button)
    return menu
