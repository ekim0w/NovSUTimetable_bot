from aiogram import types
from createTGBot import bot, dp
from DataBase import sqlite_dataBase
from aiogram.dispatcher import FSMContext
from handlers import states
from keyboards import keyboard
from handlers.admin_side import add_proxy_data


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    all_users_id = [id_[0] for id_ in await sqlite_dataBase.get_all_users()]
    if message.from_user.id not in all_users_id:
        await sqlite_dataBase.add_user(message.from_user.id)

    await bot.send_message(message.chat.id, 'Здравствуйте, я создан для помощи составления и просмотра расписания. '
                                            'Если возникли сложности или вопросы по расписанию, то вы можете обратиться к админам с помощью команды /ask_question')
    await bot.send_message(message.chat.id, 'Выберите группу в которой вы учитесь: ',
                           reply_markup=keyboard.group_keyboard(await sqlite_dataBase.get_all_groups()))
    await states.StartStates.group_name.set()


@dp.message_handler(commands=['schedule'])
async def send_my_schedule(message: types.Message):
    user_data = [u for u in await sqlite_dataBase.get_all_users() if u[0] == message.from_user.id]
    if not user_data or not user_data[0][1] or user_data[0][1] == 'no_group':
        await message.reply("Вы ещё не выбрали группу. Используй команду /select_group для выбора группы.")
        return

    group_name = user_data[0][1]
    group_data = await sqlite_dataBase.get_group(group_name)

    if not group_data or not group_data[0][1]:
        await message.reply(f"Для группы {group_name} пока нет расписания.")
        return

    schedule_text = group_data[0][1]
    await message.reply(f"📅 Расписание для группы *{group_name}*:\n\n{schedule_text}", parse_mode='Markdown')


@dp.message_handler(state=states.StartStates.group_name)
async def start_state(message: types.Message, state: FSMContext):
    all_group_names = [_[0] for _ in await sqlite_dataBase.get_all_groups()]
    if message.text in all_group_names:
        await sqlite_dataBase.change_user_group(message.from_user.id, message.text)
        await bot.send_message(message.chat.id, f'Хорошо. Я закрепил вас к группе {message.text}',
                               reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=['select_group'])
async def select_group_command(message: types.Message):
    all_groups = await sqlite_dataBase.get_all_groups()
    group_kb = keyboard.group_keyboard(all_groups)
    await message.reply('Выбери группу', reply=False,
                        reply_markup=group_kb)
    await states.SelectGroupStates.group_name.set()


@dp.message_handler(state=states.SelectGroupStates.group_name)
async def select_group_state(message: types.Message, state: FSMContext):
    all_group_names = [_[0] for _ in await sqlite_dataBase.get_all_groups()]
    if message.text in all_group_names:
        await sqlite_dataBase.change_user_group(message.from_user.id, message.text)
        await bot.send_message(message.chat.id, f'Хорошо. Группа изменена',
                               reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, 'Группу которую вы выбрали, не существует',
                               reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=['delete_me_from_group'])
async def delete_from_group(message: types.Message):
    await sqlite_dataBase.change_user_group(message.from_user.id, None)
    await message.reply('Хорошо. Группа успешно отвязана', reply=False)


@dp.message_handler(commands=['news', 'новости'])
async def news_command(message: types.Message):
    news = await sqlite_dataBase.get_news()
    for i in news[:3]:
        await bot.send_photo(message.chat.id, i[3], f'*{i[1]}*\n\n{i[2]}',
                             parse_mode='Markdown')


@dp.message_handler(commands=['ask_question'])
async def ask_question_command(message: types.Message):
    await message.reply('Напишите свой вопрос', reply=False)
    await states.AskQuestionStates.get_question.set()


@dp.message_handler(state=states.AskQuestionStates.get_question)
async def get_question_state(message: types.Message, state: FSMContext):
    await add_proxy_data(state, {
        'user_id': message.from_user.id,
        'question': message.text,
        'nickname': message.from_user.username,
    })
    await sqlite_dataBase.add_question(state)
    await message.reply('Вопрос отправлен администраторам, пожалуйста, подождите ответа...', reply=False)
    await state.finish()


@dp.message_handler(commands=['id'])
async def get_group_id(message: types.Message, state: FSMContext):
    await message.reply(message.chat.id)