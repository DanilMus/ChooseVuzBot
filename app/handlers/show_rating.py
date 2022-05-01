from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

import asyncio

from app.states import CheckState
from app.vuz import VUZ
from app.db_worker import db_worker
from app.make_vuzes_rating import make_vuzes_rating

import logging 

logger = logging.getLogger(__name__)

async def show_rating(message: types.Message, state: FSMContext):
    await message.answer('Начинаю обработку...', reply_markup= types.ReplyKeyboardRemove())

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

        # обработка ошибки со сторонним сервером
        if full_info == 'Exception':
            for i in range(3):
                await message.answer('Произошла ошибка. Проблема с сервером на стороне, подожди, пожалуйста.')
                await asyncio.sleep(100)
                full_info = await vuz.async_full_info()
                if full_info != 'Exception':
                    message.answer('Проблема решена!')
                    break
            else:
                await message.answer(
                    'Прости, пожалуйста! Проблема сильнее, чем ожидалась!'
                    'Буду рад, если дашь мне еще один шанс через некоторое время. ((('
                )
                logger.error('Жетская проблема парсинга.')
                await state.finish()

        name = full_info[0]
        # загрузили в ответ
        vuzes_data[name] = full_info[1:]
        # проверим ВУЗ в базе
        check = db_worker.get_vuz(name)
        if check: # есть ли ВУЗ в базе
            # проверяем соответствуют получение данные с базой
            if (check[0] != [tabi[i], vuzo[i], uche[i]]) and (check[1] <= 10): # какой-нибудь пользователь, однажды, ввел что-то не так
                db_worker.download_new_vuz(name, [tabi[i], vuzo[i], uche[i]], vuzes_data[name][2:])
            elif (check[2] != vuzes_data[name][2:]): # данные на сайтах обновились
                db_worker.update_info_about_vuz(name, vuzes_data[name][2:])
            else:
                db_worker.update_count_of_vuz(name)
        else: # если ВУЗа нет в базе
            db_worker.download_new_vuz(name, [tabi[i], vuzo[i], uche[i]], vuzes_data[name][2:])
    
    ####### 1.01 часть #######################
    ## (обработаем то, что ввели из базы) ####
    fromBase = user_data['chosen_vuzes_in_base']
    
    for name in fromBase:
        part_info = db_worker.get_vuz(name)
        
        vuz = VUZ(part_info[0][0], part_info[0][1], part_info[0][2], subj)
        EGE_and_budPl = await vuz.async_EGE_and_budPl()

        # обработка ошибки со сторонним сервером
        if EGE_and_budPl == 'Exception':
            for i in range(3):
                await message.answer('Произошла ошибка. Проблема с сервером на стороне, подожди, пожалуйста.')
                await asyncio.sleep(100)
                EGE_and_budPl = await vuz.async_EGE_and_budPl()
                if EGE_and_budPl != 'Exception':
                    message.answer('Проблема решена!')
                    break
            else:
                await message.answer(
                    'Прости, пожалуйста! Проблема сильнее, чем ожидалась!'
                    'Буду рад, если дашь мне еще один шанс через некоторое время. ((('
                )
                logger.error('Жесткая проблема парсинга.')
                await state.finish()

        vuzes_data[name] = EGE_and_budPl + part_info[2]

    await state.update_data(vuzes_data= vuzes_data)
    
    ###### 2 часть ###########################
    ###### (составление рейтинга ВУЗов) ######
    user_data = await state.get_data()
    criteria = user_data['chosen_criteria']
    vuzes_data = user_data['vuzes_data']
    vuzes_rating = make_vuzes_rating(criteria, vuzes_data)


    ###### 3 часть ###########################
    ###### (вывод рейтинга) ##################
    await message.answer(
        'Рейтинг готов!\n',
        reply_markup= types.ReplyKeyboardRemove()
    )
    await message.answer(
        'Вывод выглядит так:\n'
        '"Место": "ВУЗ и ссылка на него" - "баллы, которые набрал" '
        '- "на какое количество факультетов можешь поступить" / "из скольки"'
    )
    
    vuzes_rating_copy = {}
    i = len(vuzes_rating)
    top = user_data['chosen_top']

    for score1 in sorted(vuzes_rating.values()):
        for vuz, score2 in vuzes_rating.items():
            if score1[0] == score2[0]:
                vuzes_rating[vuz]
                if i <= top:
                    vuzes_rating_copy[vuz] = i
                break 
        i -= 1
        if i < 1:
            break
        await asyncio.sleep(1)
    
    i = top
    while i >= 1:
        for vuz, place in vuzes_rating_copy.items():
            if i == place:
                await message.answer(
                    f'{i} место: <a href="{vuzes_data[vuz][-1]}">{vuz}</a> - {round(vuzes_rating[vuz][0], 1)} - {vuzes_rating[vuz][1]} / {vuzes_rating[vuz][2]}',
                    disable_web_page_preview= True
                )
                i -= 1
    

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Да')
    keyboard.add('Нет')

    await message.answer(
        'Хотел бы получить больше по собранным данным?',
        reply_markup= keyboard
    )

    await state.update_data(vuzes_rating_copy = vuzes_rating_copy)
    await CheckState.waiting_for_additional_info.set()



def register_show_rating(dp: Dispatcher):
    dp.register_message_handler(show_rating, state = CheckState.waiting_for_show_rating)