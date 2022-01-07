from aiogram.dispatcher.filters.state import StatesGroup, State

class CheckState(StatesGroup):
    waiting_for_after_begining = State()
    waiting_for_put_vuz_in_mem = State()
    waiting_for_offer_subj = State()
    waiting_for_select_subj = State()
    waiting_for_select_criteria = State()