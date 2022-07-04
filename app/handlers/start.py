from aiogram import types, Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text

from app.states import states

cb = CallbackData('start', 'action')

# начало
async def start(message: types.Message, state: FSMContext):
    await message.answer('Привет', reply_markup= types.ReplyKeyboardRemove())
    await state.finish()

    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Выбрать определенные ВУЗы', callback_data= cb.new(action = 'userself')),
        types.InlineKeyboardButton('Выбрать все ВУЗы из базы', callback_data= cb.new(action = 'all')),
    ]
    keyboard.add(*buttons)

    await message.answer('Вначале мне нужно узнать куда ты хочешь поступать.', reply_markup= keyboard)

async def start_(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Выбрать определенные ВУЗы', callback_data= cb.new(action = 'userself')),
        types.InlineKeyboardButton('Выбрать все ВУЗы из базы', callback_data= cb.new(action = 'all')),
    ]
    keyboard.add(*buttons)

    await call.message.edit_text('Вначале мне нужно узнать куда ты хочешь поступать.', reply_markup= keyboard)

    await call.answer()






# выбор ВУЗов
async def all(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(vuzes_database= [])
    await state.update_data(vuzes_urls= {'tabi': [], 'vuzo': [], 'uche': []})

    database = {}
    async with state.proxy() as data:
        for vuz in database.keys():
            data['vuzes_database'].append(vuz)

    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Дальше', callback_data= cb.new(action = 'check_vuzes_FROM_all')),
        types.InlineKeyboardButton('Назад', callback_data= cb.new(action = 'start')),
    ]
    keyboard.add(*buttons)
    await call.message.edit_text('Выбрано всё.', reply_markup= keyboard)

    await call.answer()



async def userself(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(vuzes_database= [])
    await state.update_data(vuzes_urls= {'tabi': [], 'vuzo': [], 'uche': []})

    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Поиск ВУЗа в базе', switch_inline_query_current_chat= ''),
        types.InlineKeyboardButton('Дальше', callback_data= cb.new(action = 'check_vuzes_FROM_userself')), 
        types.InlineKeyboardButton('Назад', callback_data= cb.new(action = 'start')),
    ]
    keyboard.add(*buttons)

    await call.message.edit_text(
        'Ты можешь выбрать ВУЗы из базы.\n'
        'A также указать их самому по трем ссылкам с сайтов:\n'
        '<a href= "https://tabiturient.ru">tabiturient</a>\n'
        '           <a href= "https://vuzopedia.ru">vuzopedia</a>\n'
        '                       <a href= "https://ucheba.ru/for-abiturients/vuz">ucheba</a>\n'
        '!!! ВАЖНО 1 ВУЗ = 3 эти ссылки !!!\n'
        'Конда закончишь указывать, нажми: Дальше',
        reply_markup= keyboard,
        disable_web_page_preview= True
    )

    await states.vuzes.set()

    await call.answer()


async def vuzes(message: types.Message, state: FSMContext):
    database = {}

    user_text = message.text.strip()

    async with state.proxy() as data:
        if user_text in database.keys():
            data['vuzes_database'].append(user_text)
            len_vuzes_database = len(data['vuzes_database'])
            return await message.answer(f'Количество ВУЗов, полученных из базы: {len_vuzes_database}')
        
        user_text = user_text.split()
        for word in user_text:
            url ='/'.join(word.split('/')[0:5])
            if 'tabiturient.ru/vuzu/' in word:
                data['vuzes_urls']['tabi'].append(url)
            if 'vuzopedia.ru/vuz/' in word:
                data['vuzes_urls']['vuzo'].append(url)
            if 'ucheba.ru/uz/' in word:
                data['vuzes_urls']['uche'].append(url)
        
        vuzes_urls = data['vuzes_urls']
        len_vuzes_url = min(len(vuzes_urls['tabi']), len(vuzes_urls['vuzo']), len(vuzes_urls['uche']))
        return await message.answer(f'Количество ВУЗов, полученных по ссылкам: {len_vuzes_url}')


async def check_vuzes(call: types.CallbackQuery, state: FSMContext):
    FROM = call.data.split('_')[-1]

    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    button = types.InlineKeyboardButton('Назад', callback_data= cb.new(action= 'start'))
    keyboard.add(button)

    data = await state.get_data()

    vuzes_database = data['vuzes_database']
    tabi, vuzo, uche = data['vuzes_urls']['tabi'], data['vuzes_urls']['vuzo'], data['vuzes_urls']['uche']

    if (len(tabi) != len(vuzo)) or (len(tabi) != len(uche)) or (len(vuzo) != len(uche)):
        if FROM in ['userself', 'subjects']:
            return await call.message.answer('Количество введенных ссылок не совпадает.', reply_markup= keyboard)
        elif FROM == 'all':
            return await call.message.edit_text('Количество введенных ссылок не совпадает.', reply_markup= keyboard)
    if (len(tabi) < 1) and (len(vuzes_database) < 1):
        return await call.message.edit_text('Ты не указал ВУЗы.', reply_markup= keyboard)
    
    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Дальше', callback_data= cb.new(action= 'subjects')),
        types.InlineKeyboardButton('Назад', callback_data= cb.new(action= 'start')),
    ]
    keyboard.add(*buttons)

    if FROM in ['userself', 'subjects']:
        await call.message.answer('Данные введены корректно.', reply_markup= keyboard)
    elif FROM == 'all':
        await call.message.edit_text('Данные введены корректно.', reply_markup= keyboard)

    await call.answer()








# выбор предметов
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

async def subjects(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(subjects= [])
    await state.update_data(subjects_bals= {})

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add(*subj)

    await call.message.answer('Такс', reply_markup= keyboard)

    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Дальше', callback_data= cb.new(action= 'check_subjects')),
        types.InlineKeyboardButton('Назад', callback_data= cb.new(action= 'check_vuzes_FROM_subjects')),
    ]
    keyboard.add(*buttons)

    await call.message.edit_text(
        'Сейчас тебе надо будет указать предметы и баллы, на которые ты их сдаешь.'
        'Когда закончишь, нажми: Дальше.',
        reply_markup= keyboard
    )

    await states.subjects.set()


async def select_subjects(message: types.Message, state: FSMContext):
    if message.text not in subj:
        return await message.answer('Используй, пожалуйста, кнопки.')
    
    async with state.proxy() as data:
        data['subjects'].append(message.text)
    
    await message.answer('Укажи балл, предмета:')

    await states.bals.set()


async def select_bals(message: types.Message, state: FSMContext):
    user_text = message.text.strip()
    if not(user_text.isdigit()):
        return await message.answer('Введи, пожалуйста, число.')

    user_bal = int(user_text)
    if not(0 <= user_bal <= 100):
        return await message.answer('Введи, пожалуйста, настоящий бал.')
    
    async with state.proxy() as data:
        subject = data['subjects'][-1]
        data['subjects_bals'][subject] = user_bal

    await message.answer('Предмет и балл получены.')

    await states.subjects.set()

async def check_subjects(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Проверка...', reply_markup= types.ReplyKeyboardRemove())

    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Назад', callback_data= cb.new(action= 'subjects')),
    ]
    keyboard.add(*buttons)

    data = await state.get_data()
    if not(data['subjects']):
        return await call.message.answer('Ты не указал предметы.', reply_markup= keyboard)


    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Дальше', callback_data= cb.new(action= 'additional_bals')),
        types.InlineKeyboardButton('Назад', callback_data= cb.new(action= 'subjects')),
    ]
    keyboard.add(*buttons)

    await call.message.answer('Данные введены корректно.', reply_markup= keyboard)


# выбор ГТО, золотой медали
async def additional_bals(call: types.CallbackQuery, state: FSMContext):

    await state.update_data(additional_bals= [])

    keyboard = types.InlineKeyboardMarkup(row_width= 2)
    buttons = [
        types.InlineKeyboardButton('Золотая медаль и ГТО', callback_data= cb.new(action= 'additional_bals_both')),
        types.InlineKeyboardButton('ГТО', callback_data= cb.new(action= 'additional_bals_GTO')),
        types.InlineKeyboardButton('Золотая медаль', callback_data= cb.new(action= 'additional_bals_GoldMedal')),
        types.InlineKeyboardButton('Ничего', callback_data= cb.new(action= 'additional_bals_nothing')),
        types.InlineKeyboardButton('Назад', callback_data= cb.new(action= 'check_subjects')),
    ]
    keyboard.add(*buttons)

    await call.message.edit_text('Сейчас я бы хотел узнать о Золотой Медали и ГТО.', reply_markup= keyboard)

async def additional_bals_(call: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width= 1)
    buttons = [
        types.InlineKeyboardButton('Дальше', callback_data= cb.new(action= 'criteria')),
        types.InlineKeyboardButton('Назад', callback_data= cb.new(action= 'additional_bals')),
    ]
    keyboard.add(*buttons)

    choice = call.data.split('_')[-1]

    if choice == 'both':
        await state.update_data(additional_bals= ['GTO', 'GoldMedal'])
        await call.message.edit_text('Ух ты. Да ты и силен, и умен. Круто!', reply_markup= keyboard)
    elif choice == 'GTO':
        await state.update_data(additional_bals= ['GTO'])
        await call.message.edit_text('Молодец! Спорт - это жизнь!', reply_markup= keyboard)
    elif choice == 'GoldMedal':
        await state.update_data(additional_bals= ['GoldMedal'])
        await call.message.edit_text('Неплохо, неплохо.', reply_markup= keyboard)
    elif choice == 'nothing':
        await call.message.edit_text('Окей, идем дальше.', reply_markup= keyboard)




# выбор критериев
async def criteria(call: types.CallbackQuery, state: FSMContext):






async def register_start(dp: Dispatcher):
    # начало
    dp.register_message_handler(start, commands= 'start', state= '*')
    dp.register_callback_query_handler(start_, cb.filter(action= 'start'), state= '*')
    # выбор ВУЗов
    dp.register_callback_query_handler(all, cb.filter(action= 'all'), state= '*')
    dp.register_callback_query_handler(userself, cb.filter(action= 'userself'), state= '*')
    dp.register_message_handler(vuzes, state= states.vuzes)
    dp.register_callback_query_handler(check_vuzes, cb.filter(action= ['check_vuzes_FROM_all', 'check_vuzes_FROM_userself', 'check_vuzes_FROM_subjects']), state= '*')
    # выбор предметов
    dp.register_callback_query_handler(subjects, cb.filter(action= 'subjects'), state= '*')
    dp.register_message_handler(select_subjects, state= states.subjects)
    dp.register_message_handler(select_bals, state= states.bals)
    dp.register_callback_query_handler(check_subjects, cb.filter(action= 'check_subjects'), state= '*')
    # выбор ГТО, золотой медали
    dp.register_callback_query_handler(additional_bals, cb.filter(action= 'additional_bals'), state= '*')
    dp.register_callback_query_handler(additional_bals_, cb.filter(action= ['additional_bals_both', 'additional_bals_GTO', 'additional_bals_GoldMedal', 'additional_bals_nothing']), state= '*')
    # выбор критериев 