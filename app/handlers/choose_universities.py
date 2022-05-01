from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.db_worker import db_worker
from app.states import CheckState


# создание строки, где будет показываться есть ли данный ВУЗ в базе
async def select_univ(message_query: types.InlineQuery, state: FSMContext):
    data = db_worker.get_data()
    data_vuz = data.keys()

    if len(data_vuz) == 0:
        text = 'База находиться в стадии обновления.'
        just = [
            types.InlineQueryResultArticle(
                id= 'just', 
                title= text, 
                input_message_content= types.InputTextMessageContent(message_text= text),
            )
        ]
        return await message_query.answer(just, cache_time= 60)
    
    text_from_user = message_query.query

    answer = []
    for vuz in data_vuz:
        if text_from_user.lower() in vuz.lower():
            answer.append(vuz)

    articles = [
        types.InlineQueryResultArticle(
            id = vuz,
            title= vuz,
            input_message_content= types.InputTextMessageContent(message_text= vuz),
        )
        for vuz in answer
    ]

    await message_query.answer(articles, cache_time= 60)

# получает ВУЗы, в которые хочет поступить пользователь
async def put_vuz_in_mem(message: types.Message, state: FSMContext):
    data = db_worker.get_data()
    data_vuz = data.keys()
    
    # сортируем введенные данные на "есть в базе" и "нет" 
    if message.text in data_vuz:
        async with state.proxy() as data:
            data['chosen_vuzes_in_base'].append(message.text)

    else:
        what_get = message.text.split()
        
        async with state.proxy() as data:
            for elem in what_get:
                if ('https://tabiturient.ru/vuzu/' in elem):
                    new_elem = ('/'.join(elem.split('/')[0:5]))
                    data['chosen_vuzes_tabi'].append(new_elem)
                    data['check1'] = True
                elif ('https://vuzopedia.ru/vuz/' in elem):
                    new_elem = ('/'.join(elem.split('/')[0:5]))
                    data['chosen_vuzes_vuzo'].append(new_elem)
                    data['check2'] = True
                elif ('https://www.ucheba.ru/uz/' in elem):
                    new_elem = ('/'.join(elem.split('/')[0:5]))
                    data['chosen_vuzes_uche'].append(new_elem)
                    data['check3'] = True
                
                if (data['check1']) and (data['check2']) and (data['check3']):
                    data['check1'], data['check2'], data['check3'] = False, False, False
                    await message.answer('ВУЗ/ВУЗы получен/получены.')



# заканчивает получение ВУЗов
async def proverka_vuzes(message: types.Message, state: FSMContext):
    what_user_wrote = await state.get_data()

    vuzes_from_data = what_user_wrote['chosen_vuzes_in_base']
    s = ''
    for i in range(len(vuzes_from_data)):
        s += '\n' + vuzes_from_data[i]
    await message.answer(f"Вот, что вы ввели из базы: {s}") #{' '.join(vuzes_from_data)}")

    just_vuzes = what_user_wrote['chosen_vuzes_tabi'] + what_user_wrote['chosen_vuzes_vuzo'] + what_user_wrote['chosen_vuzes_uche']
    s = ''
    for i in range(len(just_vuzes)):
        s += '\n' + just_vuzes[i]
    await message.answer(f"Вот, что ввели вы: {s}", disable_web_page_preview= True) #\n{' '.join(just_vuzes)}", disable_web_page_preview= True)

    tabi = what_user_wrote['chosen_vuzes_tabi']
    vuzo = what_user_wrote['chosen_vuzes_vuzo']
    uche = what_user_wrote['chosen_vuzes_uche']
    if (len(tabi) != len(vuzo)) or (len(tabi) != len(uche)) or (len(vuzo) != len(uche)):
        await state.update_data(chosen_vuzes_in_base = [])
        await state.update_data(chosen_vuzes_tabi = [])
        await state.update_data(chosen_vuzes_vuzo = [])
        await state.update_data(chosen_vuzes_uche = [])
        return await message.answer('Количество ссылок на ВУЗы не совпадает.\nПроверь корректность данных, и введи заново.')
    if (len(tabi) < 1) and (len(vuzes_from_data) < 1):
        await state.update_data(chosen_vuzes_in_base = [])
        await state.update_data(chosen_vuzes_tabi = [])
        await state.update_data(chosen_vuzes_vuzo = [])
        await state.update_data(chosen_vuzes_uche = [])
        return await message.answer('Ты не указал ВУЗы.')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Хорошо')

    await message.answer('Данные введены корректно.\nСамое сложное позади. Теперь укажи, пожалуйста, предметы.', reply_markup= keyboard)
    await CheckState.waiting_for_offer_subj.set()


async def select_all_univ(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Хорошо')

    await message.answer('Ясненько, значит, смотрим все.\nТеперь укажи, пожалуйста, предметы.', reply_markup= keyboard)

    data = db_worker.get_data()
    data_vuz = data.keys()

    async with state.proxy() as data:
        for vuz in data_vuz:
            data['chosen_vuzes_in_base'].append(vuz)

    await CheckState.waiting_for_offer_subj.set()



def register_choose_vuz(dp: Dispatcher):
    dp.register_message_handler(proverka_vuzes, commands= 'finish1_0', state= CheckState.waiting_for_put_vuz_in_mem) #'*')
    dp.register_message_handler(select_all_univ, commands= 'finish1_1', state= CheckState.waiting_for_put_vuz_in_mem)
    dp.register_inline_handler(select_univ, state= '*') # CheckState.waiting_for_put_vuz_in_mem)
    dp.register_message_handler(put_vuz_in_mem, state= CheckState.waiting_for_put_vuz_in_mem)