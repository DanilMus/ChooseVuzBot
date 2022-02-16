from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

import asyncio

from app.states import CheckState
from app.vuz import VUZ
from app.db_worker import get_vuz, download_new_vuz

# ответные данные пользователю
vuzes_data = {} 
vuzes_rating = {}
vuzes_rating_copy = {}

def do_rating(prioritets):
    global vuzes_data, vuzes_rating
    # составляем средние значения
    print(vuzes_data)
    middle = [0] * 10
    for name, info in vuzes_data.items():
        for i in range(len(info)):
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
        if info[0] != 0:   
            score += middle[0] / info[0] * prioritets[0]
        # бюджетные места
        if middle[1] != 0:
            score += info[1] / middle[1] * prioritets[1]
        # 3 макс. балла ЕГЭ
        if info[2] != 0: 
            score += middle[2] / info[2] * prioritets[2]
        # бюджетные места на специальности 3 макс. баллов ЕГЭ
        if middle[3] != 0:
            score += info[3] / middle[3] * prioritets[3]
        # военная кафедра
        score += info[4] * prioritets[4]
        # кол-во учеников на учителя
        if info[5] != 0:
            score += middle[5] / info[5] * prioritets[5]
        # росскийский рейтинг
        if info[6] != 0:
            score += middle[6] / info[6] * prioritets[6]
        # зарубежный рейтинг
        if info[7] != 0:
            score += middle[7] / info[7] * prioritets[7]
        # отзывы
        if middle[8] != 0:
            score += info[8] / middle[8] * prioritets[8]
        # общежитие
        if middle[9] != 0:
            score += info[9] / middle[9] * prioritets[9]

        vuzes_rating[name] = score





async def the_end(message: types.Message ,state: FSMContext):
    # print('Расслабься')
    user_data = await state.get_data()

    subj = user_data['chosen_subj']
    
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
            if (proverka[5:] != full_info[5:]) and (proverka[1:3+1] != [tabi, vuzo, uche]) and (proverka[4] < 10): # если данные не совпадают и данные не прошли проверку временем
                download_new_vuz([name] + [tabi[i], vuzo[i], uche[i]] + [proverka[3] + 1] + full_info[5:])
            else: # иначе заменим данные пользователя
                vuz = VUZ(proverka[1], proverka[2], proverka[3], subj)
                full_info = await vuz.async_full_info()
                name = full_info[0]
                vuzes_data[name] = full_info[1:]
        else:
            download_new_vuz([name] + [tabi[i], vuzo[i], uche[i]] + [1] + full_info[5:])
    
    # обрабатываю то, что он ввел из базы
    from_base = user_data['chosen_vuzes_in_base']
    for name in from_base:
        part_info = get_vuz(name)
        vuz = VUZ(part_info[1], part_info[2], part_info[3], subj)
        EGE_and_bud_pl = await vuz.async_EGE_and_bud_pl()
        vuzes_data[name] = EGE_and_bud_pl + list(part_info[4:])
    
    # cоставление рейтинга ВУЗов
    prioritets = user_data['chosen_criteria']
    do_rating(prioritets)

    # вывод рейтинга
    await message.answer('Вот и закончилась подготовка рейтинга.\nЯ замедлю вывод, чтобы смотрелось эпичнее.')
    await message.answer(
        'Будет выглядеть так:\n'
        '"место": "ВУЗ" - "баллы, которые набрал"'
    )
    await asyncio.sleep(5)

    i = len(vuzes_rating)
    for score1 in sorted(vuzes_rating.values()):
        for vuz, score2 in vuzes_rating.items():
            if score1 == score2:
                await message.answer(f'{i} место: {vuz} - {round(score2)}')
                del vuzes_rating[vuz]
                vuzes_rating_copy[vuz] = i
                break
        i -= 1
        await asyncio.sleep(2)
    

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Да')
    keyboard.add('Нет')

    await message.answer('Хотел бы получить больше информации по собранным данным с твоих вузов?', reply_markup= keyboard)
    await CheckState().waiting_for_additional_info.set()

async def additional_info(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer('Замедлю, чтобы ты мог успеть все увидеть.')

        for i in range(len(vuzes_data),0,-1):
            for vuz, place in vuzes_rating_copy.items():
                if i == place:
                    info = vuzes_data[vuz]

                    await message.answer(
                        f'Вуз: {vuz}\n'
                        f'  Баллы ЕГЭ: {info[0]}\n'
                        f'  Бюджетные места: {info[1]}\n'
                        f'  3 макс. балла ЕГЭ: {info[2]}\n'
                        f'  Бюджетные места на 3 макс. балла ЕГЭ: {info[3]}\n'
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
    
    await message.answer('Большое спасибо, что воспользовался нашим ботом!\n Хорошего Тебе Дня!')
    
    await state.finish()


        



def register_the_end(dp: Dispatcher):
    dp.register_message_handler(the_end, state = CheckState.waiting_for_the_end)
    dp.register_message_handler(additional_info, state = CheckState.waiting_for_additional_info)