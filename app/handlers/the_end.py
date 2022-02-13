from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.states import CheckState
from app.vuz import vuz

async def the_end(mesage: types.Message ,state: FSMContext):
    user_data = await state.get_data()

    subj = user_data['chosen_subj']

    vuzes_data = {}
    # обрабатываем в начале то, что ввел юзер сам 
    tabi = user_data['chosen_vuzes_tabi']
    vuzo = user_data['chosen_vuzes_vuzo']
    uche = user_data['chosen_vuzes_uche']
    for i in range(len(tabi)):
        a = vuz(tabi[i],vuzo[i],uche[i], subj)
        name, EGE, bud_pl, EGE_of_3max, bud_pl_of_3max, milit_dep, stud_to_teach, rating_rus, rating_eng, obsh, reviews = a.full_info()
        vuzes_data[name] = [EGE, bud_pl, EGE_of_3max, bud_pl_of_3max, milit_dep, stud_to_teach, rating_rus, rating_eng, obsh, reviews]
        



def register_the_end(dp: Dispatcher):
    dp.register_message_handler(the_end, state = CheckState.waiting_for_the_end)