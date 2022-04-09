from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

import asyncio

from app.states import CheckState
from app.vuz import VUZ
from app.db_worker import db_worker
from app.make_vuzes_rating import make_vuzes_rating


async def show_rating(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    
    ####### 1 часть #########################
    ## (получение данных о ВУЗах) ###########
    vuzes_data = {}
    subj = user_data['chosen_subj']
    ####### 1.0 часть #######################
    # (обработаем то, что ввели по ссылкам) #
    tabi = user_data['chosen_vuzes_tabi']
    vuzo = user_data['chosen_vuzes_vuzo']
    uche = user_data['chosen_vuzes_uche']

    for i in range(len(tabi)):
        vuz = VUZ(tabi[i], vuzo[i], uche[i], subj)
        full_info = await vuz.async_full_info()
        name = full_info[0]
        # загрузили в ответ
        vuzes_data[name] = full_info[1:]
        # проверим ВУЗ в базе
        check = db_worker.get_vuz(name)
        if check: # есть ли ВУЗ в базе
            # проверяем соответствуют получение данные с базой
            if (check[0] != [tabi[i], vuzo[i], uche[i]]) and (check[1] <= 10) and (check[2] != vuzes_data[name]):
                db_worker.download_new_vuz(name, [tabi[i], vuzo[i], uche[i]], vuzes_data[name])
            else:
                db_worker.update_count_of_vuz(name)
        else: # если ВУЗа нет в базе
            db_worker.download_new_vuz(name, [tabi[i], vuzo[i], uche[i]], vuzes_data[name])
    
    ####### 1.01 часть #######################
    ## (обработаем то, что ввели из базы) ####
    fromBase = user_data['chosen_vuzes_in_base']
    for name in fromBase:
        part_info = db_worker.get_vuz(name)
        
        vuz = VUZ(part_info[0][0], part_info[0][1], part_info[0][2], subj)
        EGE_and_budPl = await vuz.async_EGE_and_budPl()
        vuzes_data = EGE_and_budPl + part_info[2]

    
    ###### 2 часть ###########################
    ###### (составление рейтинга ВУЗов) ######
    criteria = user_data['chosen_criteria']
    vuzes_rating = make_vuzes_rating(criteria, vuzes_data)