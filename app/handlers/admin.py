import asyncio
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from config.bot_config import admin

from app.db_worker import db_worker
from app.states import CheckState
from app.vuz import VUZ

logger = logging.getLogger(__name__)

async def users(message: types.Message, state: FSMContext):
    await state.finish()

    if message.from_user.id != admin:
        return await message.answer('Упс... Власть не в твоих руках.')
    
    users = db_worker.get_users()
    await message.answer(f'<b>Хозяин.</b>\nВот количество пользователей на данный момент <b>{len(users)}</b>.')

async def send_message(message: types.Message, state: FSMContext):
    await state.finish()

    if message.from_user.id != admin:
        return await message.answer('Больно многово захотел.')
    
    await message.answer('<b>Хозяин.</b>\nЧто хотите послать подданным?')

    await CheckState.waiting_for_message_from_admin.set()

async def message_from_admin(message: types.Message, state: FSMContext):
    await message.answer('<b>Хозяин. Докладываю.</b>\nСообщение получено.')

    users = db_worker.get_users()

    for id in users:
        try:
            await message.bot.send_message(chat_id= id, text= message.text)
        except Exception as ex:
            logger.error(ex)
    
    await message.answer('<b>Хозяин. Докладываю.</b>\nРасслыка закончена.')
    return await state.finish()


async def update_base(message: types.Message, state: FSMContext):
    await state.finish()

    if message.from_user.id != admin:
        return await message.answer('Слушай! Вот зачем тебе это?')

    await message.answer('<b>Хозяин. Докладываю.</b>\nНачинаю обновление базы...')

    vuzes_data = db_worker.get_data()
    
    for name, info in vuzes_data.items():
        urls = info[0]
        vuz = VUZ(urls[0],urls[1], urls[2], None)
        info_about_vuz = await vuz.async_info_to_update_base()
        if info_about_vuz == 'Exception':
            for i in range(3):
                await message.answer('Видимо сервер не пускает. Надо подождать.')
                await asyncio.sleep(100)
                info_about_vuz = await vuz.async_info_to_update_base()
                if info_about_vuz != 'Exception':
                    break
            else:
                await message.answer('Видимо, проблема, гораздо сильнее.')
                await state.finish()

        db_worker.update_info_about_vuz(name, info_about_vuz)

    await message.answer('<b>Хозяин. Докладываю.</b>\nОбновление базы завершено.')


async def look_base(message: types.Message, state: FSMContext):
    await state.finish()

    if message.from_user.id != admin:
        return await message.answer('Представлю, что этого не видел.')
    
    keyboard_inline = types.InlineKeyboardMarkup()
    keyboard_inline.add(
        types.InlineKeyboardButton(
            text= 'Посмотреть ВУЗы в базе',
            switch_inline_query_current_chat=''
        )   
    )
    await message.answer(
        '<b>Хозяин. Рад вас видеть.</b>\n'
        'Давайте посмотрим базу.',
        reply_markup= keyboard_inline
    )

    
    # await state.update_data(vuzes_data = db_worker.get_data())
    await CheckState.waiting_for_look_base_.set()


async def look_base_(message: types.Message, state: FSMContext):
    if db_worker.get_vuz(message.text):
        # admin_data = await state.get_data()
        # vuzes_data = admin_data['vuzes_data']
        ans = ''
        vuz = message.text

        vuz_info = db_worker.get_vuz(vuz)

        ans += f'<b>ВУЗ:</b> {vuz}\n\n'

        ans += f'0.0.<b>tabi:</b> {vuz_info[0][0]}\n'
        ans += f'0.1.<b>vuzo:</b> {vuz_info[0][1]}\n'
        ans += f'0.2.<b>uche:</b> {vuz_info[0][2]}\n'
        
        ans += f'\n1.<b>Счетчик:</b>  {vuz_info[1]}\n\n'

        ans += f'2.0.<b>военная кафедра:</b> {vuz_info[2][0]}\n'
        ans += f'2.1.<b>количество учеников на одного учителя:</b> {vuz_info[2][1]}\n'
        ans += f'2.2.<b>русский рейтинг:</b> {vuz_info[2][2]}\n'
        ans += f'2.3.<b>зарубежный рейтинг:</b> {vuz_info[2][3]}\n'
        ans += f'2.4.<b>отзывы:</b> {vuz_info[2][4]}\n'
        ans += f'2.5.<b>общещитие:</b> {vuz_info[2][5]}\n'
        ans += f'2.6.<b>состояние корпусов:</b> {vuz_info[2][6]}\n'
        ans += f'2.7.<b>удобство их расположения:</b> {vuz_info[2][7]}\n'
        ans += f'2.8.<b>качество образования:</b> {vuz_info[2][8]}\n'
        ans += f'2.9.<b>качество работы административного аппарата:</b> {vuz_info[2][9]}\n'
        ans += f'2.10.<b>доп активности:</b> {vuz_info[2][10]}\n'
        ans += f'2.11.<b>качество еды в столовой:</b> {vuz_info[2][11]}\n'
        ans += f'2.12.<b>средняя цена обеда:</b> {vuz_info[2][12]}\n'
        ans += f'2.13.<b>средння стоимость затрат на дорогу в месяц:</b> {vuz_info[2][13]}\n'
        ans += f'2.14.<b>Ссылка на сайт ВУЗа:</b> {vuz_info[2][14]}'

        variants = ['Стоп']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
        keyboard.add(*variants)

        await state.update_data(vuz = vuz)
        await message.answer(ans, reply_markup= keyboard)
    
    elif message.text == 'Стоп':
        await message.answer('<b>Хозяин</b>\n Спасибо за работу.', reply_markup= types.ReplyKeyboardRemove())
        await state.finish()

    else:
        return message.answer('Что-то пошло не так.')

async def show_urls(message: types.Message, state: CheckState):
    data = db_worker.get_data()
    
    s = ''
    for info in data.values():
        s += info[0][0] + '\n'
        s += info[0][1] + '\n'
        s += info[0][2] + '\n'
    
    await message.answer(s)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(users, commands= 'users', state= '*')

    dp.register_message_handler(send_message, commands= 'send_message', state= '*')
    dp.register_message_handler(message_from_admin, state= CheckState.waiting_for_message_from_admin)

    dp.register_message_handler(update_base, commands= 'update_base', state= '*')
    
    dp.register_message_handler(look_base, commands= 'look_base', state= '*')
    dp.register_message_handler(look_base_, state= CheckState.waiting_for_look_base_)

    dp.register_message_handler(show_urls, commands= 'show_urls', state= '*')