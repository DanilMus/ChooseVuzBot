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


    ###### 3 часть ###########################
    ###### (вывод рейтинга) ##################
    await message.answer(
        'Рейтинг готов!\n'
        'Вывод я замедлю, чтобы смотрелось эпичнее.'
    )
    await asyncio.sleep(3)
    await message.answer(
        'Вывод выглядит так:\n'
        '"Место": "ВУЗ" - "баллы, которые набрал" '
        '- "на какое количество факультетов можешь поступить" / "из скольки"'
    )
    await asyncio.sleep(5)
    
    vuzes_rating_copy = {}
    i = len(vuzes_rating)
    for score1 in sorted(vuzes_rating.values()):
        for vuz, score2 in vuzes_rating.items():
            if score1[0] == score2[0]:
                await message.answer(
                    f'{i} место: {vuz} - {round(score2[0], 1)} - {score2[1]} / {score2[2]}'
                )
                del vuzes_rating[vuz]
                vuzes_rating_copy[vuz] = i
                break 
        i -= 1
        await asyncio.sleep(1)
    

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Да')
    keyboard.add('Нет')

    await message.answer(
        'Хотел бы получить больше по собранным данным?',
        reply_markup= keyboard
    )

    await state.update_data(vuzes_data= vuzes_data)
    await state.update_data(vuzes_rating_copy = vuzes_rating_copy)
    await CheckState.waiting_for_additional_info.set()


async def addtional_info(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        user_data = await state.get_data()
        vuzes_data = user_data['vuzes_data']
        vuzes_rating_copy = user_data['vuzes_rating_copy']

        await message.answer(
            'Замедлю, чтобы ты мог успеть все увидеть.', 
            reply_markup= types.ReplyKeyboardRemove()
        )

        for i in range(len(vuzes_data),0,-1):
            for vuz, place in vuzes_rating_copy.items():
                if i == place:
                    info = vuzes_data[vuz]

                    await message.answer(
                        f'ВУЗ: {vuz}\n'
                        f'  баллы на факультеты для поступления: {info[0]}\n'
                        f'  количество бюджетных мест на факультеты, доступные тебе: {info[1]}\n'
                        f'  баллы на крутые факультеты: {info[2]}\n'
                        f'  бюджетные места на крутые факультеты: {info[3]}\n'
                        f'  есть или нет военной кафедры (0 или 1): {info[4]}\n'
                        f'  количество учеников на одного учителя: {info[5]}\n'
                        f'  русский рейтинг: {info[6]}\n'
                        f'  зарубежный рейтинг: {info[7]}\n'
                        f'  отзывы: {info[8]}\n'
                        f'  общещитие есть или нет (0 или 1) + отзывы (делить на 10): {info[9]}\n'
                    )

                    del vuzes_rating_copy[vuz]
                    await asyncio.sleep(7)
                    break
    
    await message.answer(
        'Большое спасибо, что воспользовался мной! )))))))'
    )

    await state.finish()




def register_the_end(dp: Dispatcher):
    dp.register_message_handler(show_rating, state = CheckState.waiting_for_show_rating.set())
    dp.register_message_handler(addtional_info, state = CheckState.waiting_for_additional_info.set())