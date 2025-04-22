from createTGBot import bot, dp
from aiogram.utils import executor
from DataBase import sqlite_dataBase
from handlers import admin_side, user_side

async def on_startup(_):
    sqlite_dataBase.sql_start()
    print("HELLO MAZAFAKA!!!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

