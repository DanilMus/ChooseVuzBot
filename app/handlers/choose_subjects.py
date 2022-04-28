from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.states import CheckState

subj = [
    "Русский язык",
    "Математика", 
    "Физика",
    "Химия",
    "История",
    "Обществознание",
    "Информатика",
    "Биология",
    "География",
    "Иностранные языки",
    "Литература"
]

async def offer_subj(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add(*subj)

    await message.answer('Выбери предметы: \nКак закончишь введи команду /finish2', reply_markup= keyboard)

    await state.update_data(chosen_subj = [])
    await CheckState.waiting_for_select_subj.set()


async def select_subj(message: types.Message, state: FSMContext):
    if message.text not in subj:
        return await message.answer('Используй, пожалуйста, кнопки.')
    
    async with state.proxy() as data:
        data['chosen_subj'].append(message.text)


async def going_to_criteria(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Oh yeah!')
    await message.answer('Что же. Предпоследний пункт.', reply_markup= keyboard)

    await state.update_data(chosen_criteria = [])
    await CheckState.waiting_for_select_criterion0.set()


def register_choose_subjects(dp: Dispatcher):
    dp.register_message_handler(going_to_criteria, commands= 'finish2', state= CheckState.waiting_for_select_subj)
    dp.register_message_handler(offer_subj, state= CheckState.waiting_for_offer_subj)
    dp.register_message_handler(select_subj, state= CheckState.waiting_for_select_subj)