from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.DataBaseWorker import DataBaseWorker

from config.bot_config import admin


async def restructure_vuzes(message: types.Message, state: FSMContext):
    await state.finish()

    if message.from_user.id != admin:
        return await message.answer('Упс... Власть не в твоих руках.')

    await message.answer('Начинаю...')

    DataBaseWorker.restructure_vuzes()

    await message.answer('Закончил')



async def register_admin(dp: Dispatcher):
    dp.register_message_handler(restructure_vuzes, commands= 'restructure_vuzes', state= '*')