from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from .. import db_worker
from app.states import CheckState


data = db_worker.get_data()
data_vuz = data.keys()


# создание строки, где будет показываться есть ли данный ВУЗ в базе
async def select_univ(message_query: types.InlineQuery, state: FSMContext):
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
                    data['chosen_vuzes'].append(new_elem)
                    data['check1'] = True
                elif ('https://vuzopedia.ru/vuz/' in elem):
                    new_elem = ('/'.join(elem.split('/')[0:5]))
                    data['chosen_vuzes'].append(new_elem)
                    data['check2'] = True
                elif ('https://www.ucheba.ru/uz/' in elem):
                    new_elem = ('/'.join(elem.split('/')[0:5]))
                    data['chosen_vuzes'].append(new_elem)
                    data['check3'] = True
                
                if data['check1'] and data['check2'] and data['check3']:
                    data['check1'], data['check2'], data['check3'] = False, False, False
                    await message.answer('ВУЗ получен.')



# заканчивает получение ВУЗов
async def proverka_vuzes(message: types.Message, state: FSMContext):
    what_user_wrote = await state.get_data()

    vuzes_from_data = what_user_wrote['chosen_vuzes_in_base']
    await message.answer(f"Вот, что вы ввели из базы:\n{' '.join(vuzes_from_data)}")

    just_vuzes = what_user_wrote['chosen_vuzes']
    await message.answer(f"Вот, что ввели вы:\n{' '.join(just_vuzes)}", disable_web_page_preview= True)

    if (len(just_vuzes) < 3) and (len(vuzes_from_data) < 1):
        return await message.answer('Вы указали слишком мало данных. Нужно начать заново. /start')

    for i in range(0, len(just_vuzes), 3):
        fir = just_vuzes[i]
        sec = just_vuzes[i+1]
        thi = just_vuzes[i+2]
        if ('tabiturient.ru' in fir) and ('vuzopedia.ru' in sec) and ('ucheba.ru' in thi):
            continue
        elif ('tabiturient.ru' in fir) and ('vuzopedia.ru' in thi) and ('ucheba.ru' in sec):
            continue
        elif ('tabiturient.ru' in sec) and ('vuzopedia.ru' in fir) and ('ucheba.ru' in thi):
            continue
        elif ('tabiturient.ru' in sec) and ('vuzopedia.ru' in thi) and ('ucheba.ru' in sec):
            continue
        elif ('tabiturient.ru' in thi) and ('vuzopedia.ru' in fir) and ('ucheba.ru' in sec):
            continue
        elif ('tabiturient.ru' in thi) and ('vuzopedia.ru' in sec) and ('ucheba.ru' in fir):
            continue
        else:
            return await message.answer(
                "Вы что-то ввели не так.\n Возможно, здесь:\n"
                f"{fir}\n {sec}\n {thi}"
                "К сожалению придется начать все сначала. /start"
            )
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Хорошо')

    await message.answer('Данные введены корректно.\nСамое сложное позади. Теперь укажи, пожалуйста, предметы.', reply_markup= keyboard)
    await CheckState.waiting_for_offer_subj.set()



def register_choose_vuz(dp: Dispatcher):
    dp.register_message_handler(proverka_vuzes, commands= 'finish1', state= CheckState.waiting_for_put_vuz_in_mem) #'*')
    dp.register_inline_handler(select_univ, state= CheckState.waiting_for_put_vuz_in_mem)
    dp.register_message_handler(put_vuz_in_mem, state= CheckState.waiting_for_put_vuz_in_mem)