from createTGBot import bot

#Удаление клавиатуры после использования
async def delete_keyboard(message):
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=None)