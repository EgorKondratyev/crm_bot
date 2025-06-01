from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard_stop_fsm(text_stop_button: str) -> InlineKeyboardMarkup:
    menu_stop = InlineKeyboardMarkup(row_width=1)
    stop_button = InlineKeyboardButton(text_stop_button, callback_data="stop_fsm")
    menu_stop.insert(stop_button)
    return menu_stop
