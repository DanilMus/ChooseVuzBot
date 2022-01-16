from aiogram.dispatcher.filters.state import StatesGroup, State

class CheckState(StatesGroup):
    waiting_for_after_begining = State()
    waiting_for_put_vuz_in_mem = State()
    waiting_for_offer_subj = State()
    waiting_for_select_subj = State()
    waiting_for_select_criterion1 = State()
    waiting_for_select_criterion2 = State()
    waiting_for_select_criterion3 = State()
    waiting_for_select_criterion4 = State()
    waiting_for_select_criterion5 = State()
    waiting_for_select_criterion6 = State()
    waiting_for_select_criterion7 = State()
    waiting_for_select_criterion8 = State()
    waiting_for_select_criterion9 = State()
    waiting_for_select_criterion10 = State()
    waiting_for_the_end = State()