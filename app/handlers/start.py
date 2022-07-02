from email.message import Message
from aiogram import types, Dispatcher
from aiogram.utils.callback_data import CallbackData

cb = CallbackData('start', 'action')


async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Выбрать всё.', callback_data= cb.new(action = 'all')),
        types.InlineKeyboardButton('Выбрать самому', callback_data= cb.new(action = 'self')),
    ]
    keyboard.add(*buttons)

    await message.answer('Привет', reply_markup= keyboard)

async def start_(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Выбрать всё.', callback_data= cb.new(action = 'all')),
        types.InlineKeyboardButton('Выбрать самому', callback_data= cb.new(action = 'self')),
    ]
    keyboard.add(*buttons)

    await call.message.edit_text('Привет', reply_markup= keyboard)


async def all(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Назад', callback_data= cb.new(action = 'start')),
    ]
    keyboard.add(*buttons)
    await call.message.edit_text('Выбрано всё.', reply_markup= keyboard)

async def self(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Назад', callback_data= cb.new(action = 'start')),
    ]
    keyboard.add(*buttons)
    await call.message.edit_text('Укажи, что хочешь взять:', reply_markup= keyboard)

async def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands= 'start')
    dp.register_callback_query_handler(start_, cb.filter(action= ['start']))
    dp.register_callback_query_handler(all, cb.filter(action= ['all']))
    dp.register_callback_query_handler(self, cb.filter(action= ['self']))