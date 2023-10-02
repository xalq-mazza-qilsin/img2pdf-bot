from aiogram.filters.state import StatesGroup, State


class Test(StatesGroup):
    get_photos = State()


class AdminState(StatesGroup):
    are_you_sure = State()
    ask_ad_content = State()
