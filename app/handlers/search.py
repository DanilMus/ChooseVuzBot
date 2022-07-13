from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.DataBaseWorker import DataBaseWorker

async def search(message_query: types.InlineQuery, state: FSMContext):
    database = DataBaseWorker.get_vuzes()

    if len(database.keys()) == 0:
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
    for vuz in database.keys():
        if text_from_user.lower() in vuz.lower():
            answer.append(vuz)
            if len(answer) > 10:
                break

    articles = [
        types.InlineQueryResultArticle(
            id = vuz,
            title= vuz,
            input_message_content= types.InputTextMessageContent(message_text= vuz),
        )
        for vuz in answer
    ]

    await message_query.answer(articles, cache_time= 60)


async def register_search(dp: Dispatcher):
    dp.register_inline_handler(search, state= '*')