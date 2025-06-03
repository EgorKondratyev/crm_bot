from aiogram.dispatcher.filters.state import State, StatesGroup


class PlacingOrderFSM(StatesGroup):
    get_shipping = State()
    get_transport = State()
    get_weight = State()
    get_width = State()
    get_height = State()
    get_destination_address = State()
    get_shipping_address = State()
