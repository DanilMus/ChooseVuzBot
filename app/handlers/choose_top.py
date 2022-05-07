from atexit import register
from email import message_from_string
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.states import CheckState


async def top(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    tabi = user_data['chosen_vuzes_tabi']
    fromBase = user_data['chosen_vuzes_in_base']
    tops = ['5', '10', '15', '20', str(len(tabi) + len(fromBase))]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add(*tops)

    await message.answer(
        'Введи топ.\n'
        'Например, 5. Тогда я выведу топ-5 (дай пять) ВУЗов для тебя.\n'
        'Надеюсь, ты понял к чему я веду.\n'
        '<i>(Можно самому ввести топ)</i>',
        reply_markup= keyboard
    )
    await CheckState.waiting_for_selected_top.set()

async def selected_top(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    tabi = user_data['chosen_vuzes_tabi']
    fromBase = user_data['chosen_vuzes_in_base']
    if (not(message.text.isdigit())) or (not(0 < int(message.text) <= (len(tabi) + len(fromBase)))):
        return await message.answer('Введи, пожалуйста, по-другому.')
    
    await state.update_data(chosen_top = int(message.text))
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Хорошо')
    
    await message.answer('Поздравляю! Осталось только дождаться результатов. \n\n<i>P.s. Это займет некоторое время.</i>', reply_markup= keyboard)
    await CheckState.waiting_for_show_rating.set()

def register_top(dp: Dispatcher):
    dp.register_message_handler(top, state= CheckState.waiting_for_top)
    dp.register_message_handler(selected_top, state= CheckState.waiting_for_selected_top)