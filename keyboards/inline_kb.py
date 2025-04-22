from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def cr_del_news_keyboards(news_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('❌ Удалить новость', callback_data=f'news {news_id}'))
    return kb

async def create_reply_keyboard(user_id):
    kb = InlineKeyboardMarkup()
    reply = InlineKeyboardButton('Ответить', callback_data=f'qtn {user_id}')
    kb.add(reply)
    return kb