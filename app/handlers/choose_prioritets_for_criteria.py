from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.states import CheckState

# async def criterion(message: types.Message, state: FSMContext, text):
#     if message.text not in buttoms:
#         return await message.answer('Нажми на кнопку, пожалуйста.')
#     async with state.proxy() as data:
#         data['chosen_criteria'].append(int(message.text))

#     await message.answer(text)

async def EGE(message: types.Message, state: FSMContext):
    await message.answer(
        'Сколько баллов ЕГЭ набрал/набираешь в сумме?',
        reply_markup= types.ReplyKeyboardRemove()
    )
    await CheckState.waiting_for_select_criterion1.set()

buttoms = ['0','1','2','3','4']

async def criterion1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bals = message.text.strip()
    if (not(bals.isdigit())) or (not(int(bals) <= (len(data['chosen_subj']) * 100 + 10))):
        return await message.answer('Неправильно ввел.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(
        "Смотри. Сейчас я буду давать тебе разные критерии (всего 18), "
        "прошу отметить, насколько они для тебя важны от 0 до 4"
    )

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add(*buttoms)

    await message.answer(
        '1. Хотел, чтобы в ВУЗе было, как можно больше факультетов, на которые ты можешь поступить?',
        reply_markup= keyboard
    )
    
    await CheckState.waiting_for_select_criterion2.set()

async def criterion2(message: types.Message, state: FSMContext):
    text = '2. Важно ли большое количество бюджетных мест?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion3.set()

async def criterion3(message: types.Message, state: FSMContext):
    text = '3. Тебе все равно на какие специальности идти (0)? Или ты хочешь на более крутые (1-4)?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion4.set()

async def criterion4(message: types.Message, state: FSMContext):
    text = '4. А что насчет количества бюджетных мест для крутых специальностей?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion5.set()

async def criterion5(message: types.Message, state: FSMContext):
    text = '5. Поговорим об армии. Насколько тебе нужна военная кафедра?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion6.set()

async def criterion6(message: types.Message, state: FSMContext):
    text = '6. Важно ли тебе, чтобы преподаватель уделял тебе время чаще? (Посмотрим сколько студентов приходится на одного учителя.)'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion7.set()

async def criterion7(message: types.Message, state: FSMContext):
    text = '7. Есть также российские рейтинги ВУЗов. Важны ли тебе они?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion8.set()

async def criterion8(message: types.Message, state: FSMContext):
    text = '8. А что насчет зарубежного рейтинга?\n(QS World University Rankings)'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion9.set()

async def criterion9(message: types.Message, state: FSMContext):
    text = '9. Ценны ли тебе отзывы об этом ВУЗе?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion10.set()

async def criterion10(message: types.Message, state: FSMContext):
    text = '10. Насколько общежитие имеет значение?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion11.set()

async def criterion11(message: types.Message, state: FSMContext):
    text = '11. Важно ли тебе состояние корпусов ВУЗа?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion12.set()

async def criterion12(message: types.Message, state: FSMContext):
    text = '12. А что насчет удобства их расположения?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion13.set()

async def criterion13(message: types.Message, state: FSMContext):
    text = '13. Качество образования?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion14.set()

async def criterion14(message: types.Message, state: FSMContext):
    text = '14. Качество работы административного аппарата?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion15.set()

async def criterion15(message: types.Message, state: FSMContext):
    text = '15. Нужны ли дополнительные активности в ВУЗе?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion16.set()

async def criterion16(message: types.Message, state: FSMContext):
    text = '16. Важно ли как кормят?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion17.set()

async def criterion17(message: types.Message, state: FSMContext):
    text = '17. Хотел бы меньше денег тратить в столовой?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_select_criterion18.set()

async def criterion18(message: types.Message, state: FSMContext):
    text = '18. А меньше тратить на дорогу?'
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(text)
    await CheckState.waiting_for_selected_criterion.set()


async def selected_criterion(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Просто нажми на нее.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Ну, ладно.')
    
    await message.answer('Все! Последний пункт!', reply_markup= keyboard)
    await CheckState.waiting_for_top.set()


def register_prioritets_for_criteria(dp: Dispatcher):
    dp.register_message_handler(EGE, state= CheckState.waiting_for_select_criterion0)
    dp.register_message_handler(criterion1, state= CheckState.waiting_for_select_criterion1)
    dp.register_message_handler(criterion2, state= CheckState.waiting_for_select_criterion2)
    dp.register_message_handler(criterion3, state= CheckState.waiting_for_select_criterion3)
    dp.register_message_handler(criterion4, state= CheckState.waiting_for_select_criterion4)
    dp.register_message_handler(criterion5, state= CheckState.waiting_for_select_criterion5)
    dp.register_message_handler(criterion6, state= CheckState.waiting_for_select_criterion6)
    dp.register_message_handler(criterion7, state= CheckState.waiting_for_select_criterion7)
    dp.register_message_handler(criterion8, state= CheckState.waiting_for_select_criterion8)
    dp.register_message_handler(criterion9, state= CheckState.waiting_for_select_criterion9)
    dp.register_message_handler(criterion10, state= CheckState.waiting_for_select_criterion10)
    dp.register_message_handler(criterion11, state= CheckState.waiting_for_select_criterion11)
    dp.register_message_handler(criterion12, state= CheckState.waiting_for_select_criterion12)
    dp.register_message_handler(criterion13, state= CheckState.waiting_for_select_criterion13)
    dp.register_message_handler(criterion14, state= CheckState.waiting_for_select_criterion14)
    dp.register_message_handler(criterion15, state= CheckState.waiting_for_select_criterion15)
    dp.register_message_handler(criterion16, state= CheckState.waiting_for_select_criterion16)
    dp.register_message_handler(criterion17, state= CheckState.waiting_for_select_criterion17)
    dp.register_message_handler(criterion18, state= CheckState.waiting_for_select_criterion18)
    dp.register_message_handler(selected_criterion, state= CheckState.waiting_for_selected_criterion)