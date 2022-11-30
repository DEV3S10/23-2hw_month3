from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import dp, bot
from keyboards.klient_kb import start_markup
from database.bot_dp import sql_command_random
from parserinio import anime


async def start_handler(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"Салалекум {message.from_user.first_name}",
                           reply_markup=start_markup)


async def info_handler(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"Сам разбирайся!")


async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data="button_call_1")
    markup.add(button_call_1)

    question = "Какая самая длинная река в мире?"
    answers = [
        "Нарын",
        "Нил",
        "Амазонка",
        "Чу",
        "Амур",
    ]

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=1,
        explanation="Учи географию",
        open_period=10,
        reply_markup=markup
    )


async def get_random_user(message: types.Message):
    await sql_command_random(message)


async def parser_cartoons(message: types.Message):
    items = anime.parser()
    for item in items:
        await message.answer(
            f"{item['link']}\n\n"
            f"{item['title']}\n"
            f"{item['status']}\n"
            f"#Y{item['year']}\n"
            f"#{item['country']}\n"
            f"#{item['genre']}\n"
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(info_handler, commands=['info'])
    dp.register_message_handler(get_random_user, commands=['get'])
    dp.register_message_handler(parser_cartoons, commands=['anime'])
