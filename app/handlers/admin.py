from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.callback_data import CallbackData

from app.DataBaseWorker import DataBaseWorker
from app.states import states

from config.bot_config import admin

import logging 

logger = logging.getLogger(__name__)

cb = CallbackData('admin', 'action')


async def admin_(message: types.Message, state: FSMContext):
    await state.finish()

    if message.from_user.id != admin:
        return await message.answer('Упс... Власть не в твоих руках.')


    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Посмортеть количество пользователей', callback_data= cb.new('users')),
        types.InlineKeyboardButton('Посмортеть количество запусков', callback_data= cb.new('launches')),
        types.InlineKeyboardButton('Отправить сообщение пользователям', callback_data= cb.new('information')),
    ]
    keyboard.add(*buttons)


    await message.answer(
        'С возвращением, Данил. \n'
        'Что хочешь посмотреть?',
        reply_markup= keyboard
    )

async def admin__(call: types.CallbackQuery, state: FSMContext):
    await state.finish()


    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Посмортеть количество пользователей', callback_data= cb.new('users')),
        types.InlineKeyboardButton('Посмортеть количество запусков', callback_data= cb.new('launches')),
        types.InlineKeyboardButton('Отправить сообщение пользователям', callback_data= cb.new('information')),
    ]
    keyboard.add(*buttons)


    await call.message.edit_text(
        'Что еще хочешь посмотреть?',
        reply_markup= keyboard
    )


async def users(call: types.CallbackQuery, state: FSMContext):
    users = DataBaseWorker.get_users()

    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    button = types.InlineKeyboardButton('Назад', callback_data= cb.new('admin'))
    keyboard.add(button)

    await call.message.edit_text(f'Количество пользователей: {len(users.keys())}', reply_markup= keyboard)


async def launches(call: types.CallbackQuery, state: FSMContext):
    users = DataBaseWorker.get_users()

    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    button = types.InlineKeyboardButton('Назад', callback_data= cb.new('admin'))
    keyboard.add(button)

    await call.message.edit_text(f'Количество запусков: {sum(users.values())}', reply_markup= keyboard)


async def information(call: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    button = types.InlineKeyboardButton('Назад', callback_data= cb.new('admin'))
    keyboard.add(button)

    await call.message.edit_text('Напиши, что хочешь послать:', reply_markup= keyboard)

    await states.information.set()

async def information_(message: types.Message, state: FSMContext):
    users = DataBaseWorker.get_users()

    for id in users:
        try: 
            await message.bot.send_message(chat_id= id, text= message.text)
        except Exception as ex:
            DataBaseWorker.del_user(id)
    





async def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_, commands= 'admin', state= '*')
    dp.register_callback_query_handler(admin__, cb.filter(action= 'admin'), state= '*')
    dp.register_callback_query_handler(users, cb.filter(action= 'users'), state= '*')
    dp.register_callback_query_handler(launches, cb.filter(action= 'launches'), state= '*')
    dp.register_callback_query_handler(information, cb.filter(action= 'information'), state= '*')
    dp.register_message_handler(information_, state= states.information)