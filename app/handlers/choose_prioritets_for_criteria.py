from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from app.states import CheckState

buttoms = ['0','1','2','3','4']

async def criterion1(message: types.Message, state: FSMContext):
    await message.answer(
        "Смотри. Сейчас я буду давать тебе разные критерии (всего 10), "
        "прошу отметить, насколько они для тебя важны от 0 до 4",
        reply_markup= types.ReplyKeyboardRemove()
    )

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add(*buttoms)

    await message.answer(
        "1. Тебе важны баллы ЕГЭ (на специальности по твоим предметам)?",
        reply_markup= keyboard
    )

    await CheckState.waiting_for_select_criterion2.set()

async def criterion2(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(
        "2. Есть еще необчный критерий.\n"
        "Скорее всего, в твоем ВУЗе куча специальностей по предметам, "
        "которые ты выбрал. И ты, наверняка, хочешь поступить на самые крутые специальности. "
        "Но на эти спецальности обычно баллы куда больше.\n"
        "Хотел бы ты выделить эти специальности? "
        '\n\nP.s.Я их называю "3 макс. балла ЕГЭ" на специальности.'
    )

    await CheckState.waiting_for_select_criterion3.set()

async def criterion3(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(
        "3. Важно ли тебе количество бюджетных мест (на специальности по твоим предметам?)"
    )

    await CheckState.waiting_for_select_criterion4.set()

async def criterion4(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(
        "4. А что на счет количества бюджетных мест на специальности "
        'с высокими баллами ("3 макс. балла ЕГЭ")?'
    )

    await CheckState.waiting_for_select_criterion5.set()

async def criterion5(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(
        "5. Поговорим об армии. Насколько тебе нужна военная кафедра?"
    )

    await CheckState.waiting_for_select_criterion6.set()

async def criterion6(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(
        "6. Важно ли тебе, чтобы преподаватель уделял тебе время чаще? "
        "(Посмотрим сколько студентов приходится на одного учителя.)"
    )

    await CheckState.waiting_for_select_criterion7.set()

async def criterion7(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(
        "7. Есть также российские рейтинги ВУЗов. "
        "Важен ли тебе они?"
    )

    await CheckState.waiting_for_select_criterion8.set()

async def criterion8(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(
        "8. А что насчет зарубежного рейтинга?\n"
        "(QS World University Rankings)"
    )

    await CheckState.waiting_for_select_criterion9.set()

async def criterion9(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))


    await message.answer(
        "9. Ценны ли тебе отзывы об этом ВУЗе?"
    )

    await CheckState.waiting_for_select_criterion10.set()

async def criterion10(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(
        "10. И последний пукт. Насколько общежитие имеет значение?"
    )

    await CheckState.waiting_for_selected_criterion.set()

async def selected_criterion(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Просто нажми на нее.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))
    
    await message.answer('Поздравляю! Осталось только дождаться результатов. \nНачинаю обработку...', reply_markup= types.ReplyKeyboardRemove())
    await CheckState.waiting_for_the_end().set()


def register_prioritets_for_criteria(dp: Dispatcher):
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
    dp.register_message_handler(selected_criterion, state= CheckState.waiting_for_the_end)