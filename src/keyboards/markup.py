from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.core.database.models.user import BusinessRelationshipType

phone_request_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton("Отправить номер телефона", request_contact=True))


def get_business_relationship_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    relationships = list(BusinessRelationshipType)

    for i in range(0, len(relationships), 3):
        row_buttons = relationships[i : i + 3]
        keyboard.row(*[KeyboardButton(rel.value) for rel in row_buttons])

    return keyboard
