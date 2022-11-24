from aiogram import Dispatcher, types
from config import dp, bot, ADMINS
from database.bot_dp import sql_command_delete, sql_command_all, sql_command_get_all_ids
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def ban(message: types.Message):
    await message.answer("Пиши в группе!")


async def delete_data(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Ты не мой БОСС!")
    else:
        users = await sql_command_all()
        for user in users:
            await bot.send_photo(
                message.from_user.id, user[6],
                caption=f"{user[2]} {user[3]} {user[4]} "
                        f"{user[5]}\n{user[1]}",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(f'delete {user[2]}',
                                         callback_data=f"delete {user[0]}")
                )
            )


async def complete_delete(call: types.CallbackQuery):
    await sql_command_delete(call.data.replace('delete ', ''))
    await call.answer(text="Удалено!", show_alert=True)
    await bot.delete_message(call.from_user.id, call.message.message_id)


async def replying(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Ты не мой БОСС!")
    else:
        user_ids = await sql_command_get_all_ids()
        for user_id in user_ids:
            await bot.send_message(user_id[0], message.text.replace('/R ', ''))


async def pin(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Ты не мой БОСС!")
    else:
        if message.reply_to_message:
            await bot.pin_chat_message(message)


async def game(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Ты не мой БОСС!")
    else:
        await bot.send_dice(message.chat.id, emoji='🎲')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix="!/")
    dp.register_message_handler(pin, commands=['pin'], commands_prefix="!")
    dp.register_message_handler(game, commands=['game'], commands_prefix="/")

    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_message_handler(replying, commands=['R'])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith("delete "))
