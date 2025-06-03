from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard_personal_area() -> InlineKeyboardMarkup:
    menu = InlineKeyboardMarkup(row_width=1)
    my_cargos_button = InlineKeyboardButton("Мои заказы", callback_data="my_cargos")
    help_button = InlineKeyboardButton(
        "Изменить информацию профиля (тех. поддержка)", url="https://example.com"
    )
    menu.insert(my_cargos_button).insert(help_button)
    return menu
