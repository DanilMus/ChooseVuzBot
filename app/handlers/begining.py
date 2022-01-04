from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class BeginingState(StatesGroup):
    waiting_start = State()

async def begining(message: types.Message, state:FSMContext):
    await state.finish()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    buttom = 'Погнали'
    keyboard.add(buttom)

    await message.answer(
        'Привет! '
        'Я помогу тебе выбрать ВУЗы, ' 
        'но только если у тебя есть список ВУЗов, '
        'и ты не можешь выбрать. Ты мне пишешь, '
        'куда  хочешь поступить, по каким предметам, ' 
        'и какие критерии тебе важны. '
        'А я тебе топ твоих ВУЗов с баллами по этим критериям.',
        reply_markup= keyboard
    )

    await BeginingState.waiting_start.set()


async def after_begining(message: types.Message, state: FSMContext):
    if message.text != 'Погнали':
        return
        
    keyboard_inline = types.InlineKeyboardMarkup()
    keyboard_inline.add(types.InlineKeyboardButton(
        text= 'Посмотреть ВУЗы в базе',
        switch_inline_query_current_chat=''
    ))
    await message.answer(
        'Начнем. Я должен узнать, куда ты хочешь постпить. '
        'Ты можешь посмотеть, какие ВУЗы есть в базе данных и указать их. '
        'Если какого-то ВУЗа нет, то надо будет указать 3 ссылки на него. '
        'С этих 3-х сайтов:\n'
        'https://tabiturient.ru\n'
        'https://vuzopedia.ru\n'
        'https://www.ucheba.ru/for-abiturients/vuz',
        reply_markup= keyboard_inline
    )

    await state.finish()


def register_begining(dp: Dispatcher):
    dp.register_message_handler(begining, commands= 'start', state= '*')
    dp.register_message_handler(after_begining)