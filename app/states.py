from aiogram.dispatcher.filters.state import StatesGroup, State

class states(StatesGroup):
    start = State()
    vuzes = State()
    subjects = State()
    bals = State()

    review = State()

    information = State()