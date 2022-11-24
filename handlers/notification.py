import aioschedule
from aiogram import types, Dispatcher
from config import bot
import asyncio


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await message.answer('Ok!')


async def go_to_sleep():
    await bot.send_message(
        chat_id=chat_id,
        text="спокойной ночи детка!"
    )


async def wake_up():
    photo = open('media/good_morning.jpeg', 'rb')
    await bot.send_photo(
        chat_id=chat_id,
        photo=photo
    )


async def scheduler():
    aioschedule.every().friday.at("23:30").do(go_to_sleep)
    aioschedule.every().monday("9:30").do(wake_up)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


def register_handlers_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id,
                                lambda word: 'notify' in word.text)
