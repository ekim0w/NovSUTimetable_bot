from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token = '7336456135:AAGmAIauHOmDxH6XCH5sTIlgPU4c933NL1U')
ADMINS_CHAT_ID = -1002696074094

dp = Dispatcher(bot, storage = storage)