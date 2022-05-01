from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.states import CheckState
from app.db_worker import db_worker

from asyncio import sleep


# дает пользовтелю инструкции
async def begining(message: types.Message, state: FSMContext):
    await state.finish()

    db_worker.add_user(message.from_user.id)

    
    # await message.answer('Привет! )))))', reply_markup= types.ReplyKeyboardRemove())
    # await message.answer(
    #     'Начнем. Вначале я должен узнать, куда ты хочешь поступить. '
    #     'Ты можешь посмотреть, какие ВУЗы есть в базе данных и указать их. ',
    #     reply_markup= keyboard_inline
    # )
    # await message.answer(
    #     'Если какого-то ВУЗа нет, то надо будет указать 3 ссылки на него. '
    #     'С этих 3-х сайтов:\n'
    #     'https://tabiturient.ru\n'
    #     'https://vuzopedia.ru\n'
    #     'https://ucheba.ru/for-abiturients/vuz\n'
    #     "<i>(Надо зайти на сайт, ввести название ВУЗа, зайти на страничку и скопировать ссылку, "
    #     "потом просто отправить сюда. Некоторое не понимают, но <b>1 ВУЗ = 3 ссылки</b>, к сожалению для вас.)</i>\n\n"
    #     "<i>Этим ты поможешь нам расширять базу данных.</i>",
    #     disable_web_page_preview= True
    # )
    # await sleep(0.2)
    # await message.answer('Когда закончишь указывать введи команду -> /finish1_0.')
    # await sleep(0.2)
    # await message.answer('А можешь вообще все ВУЗы указать, нажав сюда -> /finish1_1.')

    await message.answer(
        'Привет! )))))\n'
        'Для начала, давай я узнаю, куда ты хочешь поступить.', 
        reply_markup= types.ReplyKeyboardRemove()
    )
    # await sleep(1)
    await message.answer(
        'Есть 3 способа указать ВУЗы.'
    )
    # await sleep(1)
    await message.answer(
        'Первый. Можно указать ВУЗ по 3 ссылкам:\n'
        'https://tabiturient.ru\n'
        'https://vuzopedia.ru\n'
        'https://ucheba.ru/for-abiturients/vuz\n'
        '<i>(Уточню, что 1 ВУЗ = 3 ссылки)</i>',
        disable_web_page_preview= True
    )
    
    keyboard_inline = types.InlineKeyboardMarkup()
    keyboard_inline.add(
        types.InlineKeyboardButton(
            text= 'Посмотреть ВУЗы в базе',
            switch_inline_query_current_chat=''
        )   
    )
    await message.answer(
        'Второй. Просто посмотреть, какие ВУЗы есть в базе, и указать их.'
    )
    await message.answer(
        'Третий. Можно выбрать <i>абсолютно</i> все ВУЗы из моей базы, нажав сюда ->  /finish1_1.',
        reply_markup= keyboard_inline
    )
    # await sleep(3)
    await message.answer(
        'Для 2 и 3 способа надо нажать -> /finish1_0, когда закончишь вводить <i>ВСЕ</i> ВУЗы'
    )


    # запоминаение того, что ввел пользователь
    await state.update_data(chosen_vuzes_in_base = [])
    await state.update_data(chosen_vuzes_tabi = [])
    await state.update_data(chosen_vuzes_vuzo = [])
    await state.update_data(chosen_vuzes_uche = [])

    await CheckState.waiting_for_put_vuz_in_mem.set()

    await state.update_data(check1 = False)
    await state.update_data(check2 = False)
    await state.update_data(check3 = False)



def register_introduction(dp: Dispatcher):
    dp.register_message_handler(begining, commands= 'start', state= '*')