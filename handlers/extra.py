from aiogram import Dispatcher, types
from config import dp, bot


async def echo(message: types.Message):
    bad_words = ['html', 'css', 'js', 'java', "дурак"]
    username = f"@{message.from_user.username}" if message.from_user.username is not None \
        else message.from_user.full_name

    for word in bad_words:
        if word in message.text.lower():
            await message.answer(f'Не матерись {username} '
                                 f'сам ты {word}')

    if message.text.startswith('.'):
        await bot.pin_chat_message(message.chat.id, message.message_id)

    if message.text == "dice":
        await bot.send_dice(message.chat.id, emoji='🎲')


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(echo)
