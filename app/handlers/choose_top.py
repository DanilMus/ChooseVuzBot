from atexit import register
from email import message_from_string
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.states import CheckState


async def top(message: types.Message, state: FSMContext):
    tops = ['5', '10', '15', '20']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add(*tops)

    await message.answer(
        'Введи топ.\n'
        'Например, 5. Тогда я выведу топ-5 дай пять ВУЗов для тебя.'
        'Надеюсь, ты понял к чему я веду.\n'
        '<i>(Максимальный топ - это 20, для твоего же удобства)</i>',
        reply_markup= keyboard
    )
    await CheckState.waiting_for_selected_top.set()

async def selected_top(message: types.Message, state: FSMContext):
    if (not(message.text.isdigit())) and (not(int(message.text) <= 20)):
        return await message.answer('Введи, пожалуйста, нормально.')
    
    await state.update_data(chosen_top = int(message.text))
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Хорошо')
    
    await message.answer('Поздравляю! Осталось только дождаться результатов. \nНачинаю обработку...\n\n<i>P.s. Это займет некоторое время.</i>', reply_markup= keyboard)
    await CheckState.waiting_for_show_rating.set()

def register_top(dp: Dispatcher):
    dp.register_message_handler(top, state= CheckState.waiting_for_top)
    dp.register_message_handler(selected_top, state= CheckState.waiting_for_selected_top)