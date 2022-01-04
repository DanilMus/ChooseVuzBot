from aiogram import types, Dispatcher
from .. import db_worker

# создание строки, где будет показываться есть ли данный ВУЗ в базе
async def select_univ(message_query: types.InlineQuery):
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


def register_select_vuz_func(dp: Dispatcher):
    dp.register_inline_handler(select_univ)