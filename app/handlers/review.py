from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.states import states

from config.bot_config import admin



async def review(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(
        'Привет. Просто напиши о том, что хотел бы изменить, улучшить.'
    )

    await states.review.set()


async def review_(message: types.Message, state: FSMContext):
    await message.bot.send_message(
        chat_id= admin,
        text = f'Отзыв:\n{message.text}'
    )

    await message.answer('Отзыв получен и отправлен. Спасибо большое тебе за него. Это поможет мне развиваться.')

    await state.finish()




async def register_review(dp: Dispatcher):
    dp.register_message_handler(review, commands= 'review', state= '*')
    dp.register_message_handler(review_, state= states.review)