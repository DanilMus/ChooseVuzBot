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
        "1. Тебе важны низкие баллы ЕГЭ (на специальности по твоим предметам)?",
        reply_markup= keyboard
    )

    await CheckState.waiting_for_select_criterion2.set()

async def criterion2(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(
        "2. Важно ли тебе большое количество бюджетных мест (на специальности по твоим предметам?)"
    )

    await CheckState.waiting_for_select_criterion3.set()

async def criterion3(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))


    await message.answer(
        "3. Необычный критерий. (Прости, что так много написал, я уже отчаился в попытках объяснить его.)\n"
        "Чтобы лучше понять его, приведу пример. "
        'Допустим, ты хочешь поступить в "МГТУ имени Баумана" по предметам: '
        "русский, математика, информатика.\n"
        "Но там очень много специальностей для поступления с такими предметами, "
        'и самое важное, что ты скорее всего не хочешь на какое-нибудь "энергитическое машиностроение".\n'
        "А у меня есть выход.\n"
        "И я тебя спрашиваю, хотел бы ты отделить то, что тебе, скорее всего, не пригодиться?\n\n"
        "P.s. Мне достаточно взять несколько специальностей с максимальными баллами и выделить их, а "
        "специльности с маленькими, куда ты, наверное, не хочешь, я просто не учту в этом критерии."
    )

    await CheckState.waiting_for_select_criterion4.set()

async def criterion4(message: types.Message, state: FSMContext):
    if message.text not in buttoms:
        return await message.answer('Нажми на кнопку, пожалуйста.')
    async with state.proxy() as data:
        data['chosen_criteria'].append(int(message.text))

    await message.answer(
        "4. Этот критерий связан с предыдущим.\n"
        'Важно ли тебе большое количество бюджетных мест есть на эти "особенные" специльности?'
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

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    keyboard.add('Хорошо')
    
    await message.answer('Поздравляю! Осталось только дождаться результатов. \nНачинаю обработку...\n\nP.s. Это займет, примерно, 10-15 минут.\nТак что можешь пока попить чайку.', reply_markup= keyboard)
    await CheckState.waiting_for_the_end.set()


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
    dp.register_message_handler(selected_criterion, state= CheckState.waiting_for_selected_criterion)