from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from config.bot_config import admin

from app.db_worker import db_worker
from app.states import CheckState



async def users(message: types.Message, state: FSMContext):
    await state.finish()

    if message.from_user.id != admin:
        return message.answer('Упс... Власть не в твоих руках.')
    
    users = db_worker.get_users()
    await message.answer(f'<b>Хозяин.</b>\nВот количество пользователей на данный момент <b>{len(users)}</b>.')

async def send_message(message: types.Message, state: FSMContext):
    await state.finish()

    if message.from_user.id != admin:
        return message.answer('Больно многово захотел.')
    
    await message.answer('<b>Хозяин.</b>\nЧто хотите послать подданным?')

    await CheckState.waiting_for_message_from_admin.set()

async def message_from_admin(message: types.Message, state: FSMContext):
    await message.answer('<b>Хозяин. Докладываю.</b>\nСообщение получено.')

    users = db_worker.get_users()

    for id in users:
        await message.bot.send_message(chat_id= id, text= message.text)
    
    await message.answer('<b>Хозяин. Докладываю.</b>\nРасслыка закончена.')
    return await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(users, commands= 'users', state= '*')
    dp.register_message_handler(send_message, commands= 'send_message', state= '*')
    dp.register_message_handler(message_from_admin, state= CheckState.waiting_for_message_from_admin)