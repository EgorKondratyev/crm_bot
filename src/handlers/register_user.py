from aiogram import types
from aiogram.dispatcher import FSMContext

from src.core.bot.bot import dp
from src.core.database.models.user import BusinessRelationshipType
from src.dao.user import UserDAO
from src.keyboards.inline.stop import create_keyboard_stop_fsm
from src.keyboards.markup import get_business_relationship_keyboard
from src.states.register import RegisterFSM


async def contact_handler(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    async with state.proxy() as data:
        data["phone_number"] = phone_number
    await message.answer(
        f"Ваш контактный номер для службы поддержки: <b>{phone_number}</b>\n\n"
        f"*Если необходимо сменить номер Вашего аккаунта, то свяжитесь с нашей тех. поддержкой",
        parse_mode="html",
        reply_markup=get_business_relationship_keyboard(),
    )
    await RegisterFSM.get_company_type.set()
    await message.answer(
        f"Для дальнейших шагов укажите <b>тип бизнес модели</b> Вашей компании по одной из кнопок ниже 👇",
        reply_markup=create_keyboard_stop_fsm(
            text_stop_button="🛑Остановить процесс регистрации🛑"
        ),
        parse_mode="html",
    )


async def company_type_handler(message: types.Message, state: FSMContext):
    company_type = message.text
    if not any(company_type == item.value for item in BusinessRelationshipType):
        await message.answer(
            "Такого типа бизнес модели не существует! Напишите корректный тип бизнес модели или остановите регистрацию",
            reply_markup=create_keyboard_stop_fsm(
                text_stop_button="🛑Остановить процесс регистрации🛑"
            ),
        )
        return
    async with state.proxy() as data:
        phone_number = data["phone_number"]

    await UserDAO.add(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        surname=message.from_user.username,
        phone_number=phone_number,
        business_type=company_type,
    )
    await state.finish()
    await message.answer("🎊")
    await message.answer(
        "Благодарим за успешную регистрацию в нашем сервисе\n\n"
        "Для создания заявки на перевозку, выберите соответсвующий раздел в панели кнопок клиента"
    )


def register_register_handlers():
    dp.register_message_handler(
        contact_handler,
        content_types=types.ContentType.CONTACT,
        state=RegisterFSM.get_phone,
    )
    dp.register_message_handler(
        company_type_handler,
        state=RegisterFSM.get_company_type,
    )
