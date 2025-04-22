from createTGBot import bot
from DataBase import sqlite_dataBase

async def sending_schedule(name):
    users = await sqlite_dataBase.get_only_such_users(name)
    group = await sqlite_dataBase.get_group(name)
    schedule_text = group[0][1]
    for user in users:
        user_id = user[0]
        await bot.send_message(user_id, f'РАСПИСАНИЕ ВАШЕЙ ГРУППЫ ОБНОВЛЕНО\n\n{schedule_text}')