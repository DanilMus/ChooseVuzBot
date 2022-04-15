from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

import asyncio

from app.states import CheckState


async def show_addtinal_info(message: types.Message, i, vuzes_rating_copy, vuzes_data):
    for vuz, place in vuzes_rating_copy.items():
        if i == place:
            info = vuzes_data[vuz]

            await message.answer(
                f'ВУЗ: {vuz}\n'
                f'  баллы на факультеты для поступления: {info[0]}\n'
                f'  количество бюджетных мест на факультеты, доступные тебе: {info[1]}\n'
                f'  баллы на крутые факультеты: {info[2]}\n'
                f'  бюджетные места на крутые факультеты: {info[3]}\n'
                f'  есть или нет военной кафедры (0 или 1): {info[4]}\n'
                f'  количество учеников на одного учителя: {info[5]}\n'
                f'  русский рейтинг: {info[6]}\n'
                f'  зарубежный рейтинг: {info[7]}\n'
                f'  отзывы: {info[8]}\n'
                f'  общещитие есть или нет (0 или 1) + отзывы (делить на 10): {info[9]}\n'
            )

            del vuzes_rating_copy[vuz]
            break
    

async def additional_info(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        user_data = await state.get_data()
        vuzes_data = user_data['vuzes_data']
        vuzes_rating_copy = user_data['vuzes_rating_copy']
        i = len(vuzes_data) 

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
        keyboard.add('Дальше')
        await message.answer(
            'Чтобы смотреть дальше просто нажми кнопку "Дальше".',
            reply_markup= keyboard
        )
        await show_addtinal_info(message, i, vuzes_rating_copy, vuzes_data)

        await state.update_data(i= i-1)
        await CheckState.waiting_for_additional_info_.set()
    else:
        await the_end(message, state)

async def additional_info_(message: types.Message, state: FSMContext):
    if message.text != 'Дальше':
        return message.answer('Нажми на кнопку!')

    user_data = await state.get_data()
    vuzes_data = user_data['vuzes_data']
    vuzes_rating_copy = user_data['vuzes_rating_copy']
    i = user_data['i']

    await show_addtinal_info(message, i, vuzes_rating_copy, vuzes_data)
    if i - 1 != 0:
        await state.update_data(i= i-1)
    else:
        await CheckState.waiting_for_the_end.set()


async def the_end(message: types.Message, state: FSMContext):
    await message.answer(
        'Большое спасибо, что воспользовался мной! )))))))',
        reply_markup= types.ReplyKeyboardRemove()
    )
    await state.finish()


def register_the_end(dp: Dispatcher):
    dp.register_message_handler(additional_info, state = CheckState.waiting_for_additional_info)
    dp.register_message_handler(additional_info_, state = CheckState.waiting_for_additional_info_)
    dp.register_message_handler(the_end, state= CheckState.waiting_for_the_end)