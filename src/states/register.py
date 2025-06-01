from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterFSM(StatesGroup):
    get_phone = State()
    get_company_type = State()
    # TODO: email
