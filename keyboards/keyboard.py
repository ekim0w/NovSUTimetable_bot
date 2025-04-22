from aiogram import types

def group_keyboard(group_list):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for group in group_list:
        butt = types.KeyboardButton(group[0])
        kb.add(butt)
    return kb