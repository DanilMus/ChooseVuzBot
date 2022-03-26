from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.states import CheckState

from asyncio import sleep

# самое начало, вводит пользователя в курс дела
async def begining(message: types.Message, state: FSMContext):
    await state.finish()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    buttom = "Okay. Let's go!"
    keyboard.add(buttom)

    await message.answer(
        'Привет!\n'
        'Я помогу тебе выбрать ВУЗы, ' 
        'но только если у тебя есть список ВУЗов, '
        'и ты не можешь выбрать, в какие поступать.\nТы мне пишешь, '
        'куда  хочешь поступить, по каким предметам, ' 
        'и какие критерии тебе важны. '
        'А я тебе топ твоих ВУЗов с баллами по этим критериям.\n\n'
        'P.s. В левом нижнем углу есть 3 полоски, если на них нажать, то получишь список команд.',
        reply_markup= keyboard
    )

    await CheckState.waiting_for_after_begining.set()


# дает пользовтелю инструкции
async def after_begining(message: types.Message, state: FSMContext):
    await message.answer("Окей", reply_markup= types.ReplyKeyboardRemove())
    await sleep(0.2)

    keyboard_inline = types.InlineKeyboardMarkup()
    keyboard_inline.add(types.InlineKeyboardButton(
        text= 'Посмотреть ВУЗы в базе',
        switch_inline_query_current_chat=''
    ))
    await message.answer(
        'Начнем. Я должен узнать, куда ты хочешь поступить. '
        'Ты можешь посмотреть, какие ВУЗы есть в базе данных и указать их. '
        'Если какого-то ВУЗа нет, то надо будет указать 3 ссылки на него. '
        'С этих 3-х сайтов:\n'
        'https://tabiturient.ru\n'
        'https://vuzopedia.ru\n'
        'https://ucheba.ru/for-abiturients/vuz\n'
        "(Надо зайти на сайт, ввести название ВУЗа, зайти на страничку и скопировать ссылку, "
        "потом просто отправить сюда.)\n\n"
        "Этим ты поможешь нам расширять базу данных.",
        reply_markup= keyboard_inline,
        disable_web_page_preview= True
    )
    await sleep(0.2)
    await message.answer('Когда закончишь указывать введи команду /finish1.')

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
    dp.register_message_handler(after_begining, state= CheckState.waiting_for_after_begining)