from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

import asyncio

from app.states import CheckState
from app.vuz import VUZ
from app.db_worker import get_vuz, download_new_vuz, update_count_of_vuz


# обработавыем баллы ЕГЭ и бюджетные места
def EGE(EGE_now:int, EGE:list, bud_pl:list, EGE_of_3max:list, bud_pl_of_3max:list):
    count = len(EGE) # общее количество
    count_where_can = 0 # только куда можешь посупить 
    buds = 0 # количество бюджетных мест, куда можешь поступить

    for i in range(len(EGE)):
        bal = EGE[i]
        bud = bud_pl[i]

        if EGE_now >= (bal - 2):
            count_where_can += 1
            buds += bud 
    
    count_where_can_of_3max = 0 # только куда можешь посупить 
    buds_of_3max = 0 # количество бюджетных мест, куда можешь поступить
    for i in range(len(EGE_of_3max)):
        bal = EGE_of_3max[i]
        bud = bud_pl_of_3max[i]

        if EGE_now >= (bal - 2):
            count_where_can_of_3max += 1
            buds_of_3max += bud

    return [[count, count_where_can] , buds, count_where_can_of_3max, buds_of_3max]


def do_rating(prioritets, vuzes_data):
    # составляем средние значения
    middle = [0] * 10
    for name, info in vuzes_data.items():
        for i in range(1, len(info)): # без баллов ЕГЭ
            middle[i] += info[i] 
    count = len(vuzes_data)
    for i in range(len(middle)):
        middle[i] /= count

    # делаем рейтинг
    # если чем больше тем лучше, то знач / ср.знач. (vuzes_data / middle)
    # если чем меньше тем лучше, то ср.знач. / знач. (middle / vuzes_data)
    vuzes_rating = {}
    for name, info in vuzes_data.items():
        score = 0
        # баллые ЕГЭ
        if info[0][1] != 0:
            score += 20  
        # бюджетные места
        if middle[1] != 0:
            score += info[1] / middle[1] * prioritets[1]
        # 3 макс. балла ЕГЭ
        if info[2] != 0: 
            score += middle[2] / info[2] * prioritets[2]
        # бюджетные места на специальности 3 макс. баллов ЕГЭ 
        if middle[3] != 0:
            score += info[3] / middle[3] * prioritets[1] # (критерий берем из обычных бюджетных мест)
        # военная кафедра
        score += info[3] * prioritets[3]
        # кол-во учеников на учителя
        if info[5] != 0:
            score += middle[5] / info[5] * prioritets[4]
        # росскийский рейтинг
        if info[6] != 0:
            score += middle[6] / info[6] * prioritets[5]
        # зарубежный рейтинг
        if info[7] != 0:
            score += middle[7] / info[7] * prioritets[6]
        # отзывы
        if middle[8] != 0:
            score += info[8] / middle[8] * prioritets[7]
        # общежитие
        if middle[9] != 0:
            score += info[9] / middle[9] * prioritets[8]

        vuzes_rating[name] = score
    
    return vuzes_rating





async def the_end(message: types.Message ,state: FSMContext):
    # ответные данные пользователю
    vuzes_data = {} 
    vuzes_rating_copy = {}


    user_data = await state.get_data()

    subj = user_data['chosen_subj']
    ############## 1 часть ####################
    # обрабатываем в начале то, что ввел юзер сам 
    tabi = user_data['chosen_vuzes_tabi']
    vuzo = user_data['chosen_vuzes_vuzo']
    uche = user_data['chosen_vuzes_uche']
    for i in range(len(tabi)):
        # получаю новые данные
        vuz = VUZ(tabi[i], vuzo[i], uche[i], subj)
        full_info = await vuz.async_full_info()
        name = full_info[0]
        vuzes_data[name] = full_info[1:]
        # загружаю их в базу, если надо
        proverka = get_vuz(name)
        if proverka: # есть ли ВУЗ в базе
            if (proverka[4:] != full_info[4:]) and (proverka[1:2+1] != [tabi, vuzo, uche]) and (proverka[3] < 10): # если данные не совпадают и данные не прошли проверку временем
                download_new_vuz([name] + [tabi[i], vuzo[i], uche[i]] + [1] + full_info[5:])
            else: # если все ОК
                update_count_of_vuz(name, proverka[3] + 1)
        else: # если ВУЗа нет в базе 
            download_new_vuz([name] + [tabi[i], vuzo[i], uche[i]] + [1] + full_info[5:])
    
    # обрабатываю то, что он ввел из базы
    from_base = user_data['chosen_vuzes_in_base']
    for name in from_base:
        part_info = get_vuz(name)
        if part_info:
            vuz = VUZ(part_info[0], part_info[1], part_info[2], subj)
            EGE_and_bud_pl = await vuz.async_EGE_and_bud_pl()
            vuzes_data[name] = EGE_and_bud_pl + list(part_info[4:])
    


    ############## 2 часть ####################
    # cоставление рейтинга ВУЗов
    prioritets = user_data['chosen_criteria']
    EGE_now = prioritets[0]
    for key, val in vuzes_data.items():
        vuzes_data[key] =  EGE(EGE_now, val[0], val[1], val[2], val[3]) + val[4:]

    vuzes_rating = do_rating(prioritets, vuzes_data)



    ############## 3 часть ####################
    # вывод рейтинга
    await message.answer('Вот и закончилась подготовка рейтинга.\nЯ замедлю вывод, чтобы смотрелось эпичнее.')
    await message.answer(
        'Будет выглядеть так:\n'
        '"место": "ВУЗ" - "баллы, которые набрал" - "на какое количество факультетов можешь поступить"'
    )
    await asyncio.sleep(5)

    i = len(vuzes_rating)
    for score1 in sorted(vuzes_rating.values()):
        for vuz, score2 in vuzes_rating.items():
            if score1 == score2:
                await message.answer(f'{i} место: {vuz} - {round(score2)} - {vuzes_data[vuz][0][1]}/{vuzes_data[vuz][0][0]}')
                del vuzes_rating[vuz]
                vuzes_rating_copy[vuz] = i
                break
        i -= 1
        await asyncio.sleep(2)
    

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Да')
    keyboard.add('Нет')

    await message.answer('Хотел бы получить больше информации по собранным данным с твоих вузов?', reply_markup= keyboard)

    await state.update_data(vuzes_data= vuzes_data)
    await state.update_data(vuzes_rating_copy= vuzes_rating_copy)
    await CheckState().waiting_for_additional_info.set()



async def additional_info(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        user_data = await state.get_data()
        vuzes_data = user_data['vuzes_data']
        vuzes_rating_copy = user_data['vuzes_rating_copy']

        await message.answer('Замедлю, чтобы ты мог успеть все увидеть.', reply_markup= types.ReplyKeyboardRemove())

        for i in range(len(vuzes_data),0,-1):
            for vuz, place in vuzes_rating_copy.items():
                if i == place:
                    info = vuzes_data[vuz]

                    await message.answer(
                        f'Вуз: {vuz}\n'
                        f'  На сколько из скольки факультетов можешь поступить: {info[0][1]}/{info[0][0]}\n'
                        f'  Бюджетные места на эти факультеты: {info[1]}\n'
                        f'  Количество крутых факультов, на которые можешь поступить: {info[2]}\n'
                        f'  Бюджетные места на эти крутые факультеты: {info[3]}\n'
                        f'  Военная кафедра: {info[4]}\n'
                        f'  Количествово учеников на 1-го учителя: {info[5]}\n'
                        f'  Российский рейтинг: {info[6]}\n'
                        f'  Западный рейтинг: {info[7]}\n'
                        f'  Отзывы: {info[8]}\n'
                        f'  Общежитие: {info[9]}\n'
                    )

                    del vuzes_rating_copy[vuz]
                    await asyncio.sleep(7)
                    break
    
    await message.answer('Большое спасибо, что воспользовался нашим ботом!\n Хорошего Тебе Дня!', reply_markup= types.ReplyKeyboardRemove())
    
    await state.finish()


        



def register_the_end(dp: Dispatcher):
    dp.register_message_handler(the_end, state = CheckState.waiting_for_the_end)
    dp.register_message_handler(additional_info, state = CheckState.waiting_for_additional_info)