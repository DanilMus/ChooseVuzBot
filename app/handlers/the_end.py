from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

import asyncio
import logging

from app.states import CheckState

from config.bot_config import admin

logger = logging.getLogger(__name__)

async def show_addtinal_info(message: types.Message, i, vuzes_rating_copy, vuzes_data):
    for vuz, place in vuzes_rating_copy.items():
        if i == place:
            info = vuzes_data[vuz]

            faculties = info[0]
            faculties_of3max = info[1]

            textAbout_faculties = ''
            textAbout_faculties_of3max = ''

            for faculty_name, faculty_info in faculties.items():
                textAbout_faculties += f'      {faculty_name}: {faculty_info[0]}, {faculty_info[1]}\n'
            
            for faculty_name, faculty_info in faculties_of3max.items():
                textAbout_faculties_of3max += f'      {faculty_name}: {faculty_info[0]}, {faculty_info[1]}\n'

            await message.answer(
                f'<b>Место:</b> {place}\n'
                f'<b>>ВУЗ:</b> <a href="{vuzes_data[vuz][-1]}">{vuz}</a>\n\n'
                f'<b>>>>факультеты с баллами ЕГЭ и бюджетными местами на них:</b>\n{textAbout_faculties}\n'
                f'<b>>>>крутые факультеты and баллы and бюджетные места на них:</b>\n{textAbout_faculties_of3max}\n'
                f'<b>>>>есть или нет военной кафедры (0 или 1):</b> {info[2]}\n'
                f'<b>>>>количество учеников на одного учителя:</b> {info[3]}\n'
                f'<b>>>>русский рейтинг:</b> {info[4]}\n'
                f'<b>>>>зарубежный рейтинг:</b> {info[5]}\n'
                f'<b>>>>отзывы:</b> {info[6]}\n'
                f'<b>>>>общещитие есть или нет (0 или 1) + отзывы (делить на 10):</b> {info[7]}\n'
                f'<b>>>>состояние корпусов:</b> {info[8]}\n'
                f'<b>>>>удобство расположения корпусов:</b> {info[9]}\n'
                f'<b>>>>качество образования:</b> {info[10]}\n'
                f'<b>>>>качество работы административного аппарата:</b> {info[11]}\n'
                f'<b>>>>доп активности:</b> {info[12]}\n'
                f'<b>>>>качество еды в столовой:</b> {info[13]}\n'
                f'<b>>>>средняя цена обеда:</b> {info[14]}\n'
                f'<b>>>>средння стоимость затрат на дорогу в месяц:</b> {info[15]}\n'
            )

            del vuzes_rating_copy[vuz]
            break
    

async def additional_info(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        user_data = await state.get_data()
        vuzes_data = user_data['vuzes_data']
        vuzes_rating_copy = user_data['vuzes_rating_copy']
        
        i = len(vuzes_rating_copy)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
        keyboard.add('Дальше')
        await message.answer(
            'Чтобы смотреть дальше просто нажми кнопку "Дальше".',
            reply_markup= keyboard
        )
        await message.answer(
            'Отмечу, что на некоторые специальности баллы могут быть куда больше, '
            'чем ожидалось. Скорее всего это из-за того, что '
            'надо сдавать вступительные экзамены.'
        )
        await show_addtinal_info(message, i, vuzes_rating_copy, vuzes_data)

        await state.update_data(i= i-1)
        await CheckState.waiting_for_additional_info_.set()
    else:
        await message.answer(
            'Можешь, пожалуйста, написать все, что не понравилось? <i>(Я все равно не узнаю, кто ты, так что домой к тебе не приду))</i>',
            reply_markup= types.ReplyKeyboardRemove()
        )
        await CheckState.waiting_for_the_end.set()
        # await the_end(message, state)

async def additional_info_(message: types.Message, state: FSMContext):
    if message.text != 'Дальше':
        return message.answer('Нажми на кнопку!')

    user_data = await state.get_data()
    vuzes_data = user_data['vuzes_data']
    vuzes_rating_copy = user_data['vuzes_rating_copy']
    i = user_data['i']

    await show_addtinal_info(message, i, vuzes_rating_copy, vuzes_data)
    if i - 1 > 0:
        await state.update_data(i= i-1)
    else:
        # await asyncio.sleep(5)
        await message.answer(
            'Если я тебе понравился, буду рад, если расскажешь обо мне другу! Так я смогу расти и предлагать все более крутые вещи.'
        )
        await message.answer(
            'Можешь, пожалуйста, написать все, что не понравилось? <i>(Я все равно не узнаю, кто ты, так что домой к тебе не приду))</i>',
            reply_markup= types.ReplyKeyboardRemove()
        )
        await CheckState.waiting_for_the_end.set()


async def the_end(message: types.Message, state: FSMContext):
    logger.info(f'Отзыв: \n{message.text}')
    try:
        await message.bot.send_message(
            chat_id= admin,
            text = f'Отзыв:\n{message.text}'
        )
    except Exception as ex:
        logger.error(ex)
    await message.answer(
        'Семпай, Большое Cпасибо, что воспользовался мной! )))))))',
        reply_markup= types.ReplyKeyboardRemove()
    )
    await state.finish()


def register_the_end(dp: Dispatcher):
    dp.register_message_handler(additional_info, state = CheckState.waiting_for_additional_info)
    dp.register_message_handler(additional_info_, state = CheckState.waiting_for_additional_info_)
    dp.register_message_handler(the_end, state= CheckState.waiting_for_the_end)