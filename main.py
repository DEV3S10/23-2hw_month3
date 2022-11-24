from aiogram import executor
from config import dp
import logging
from handlers import client, callback, extra, admin, fsmAdminMentor
from database.bot_dp import sql_create


async def on_startup(_):
    sql_create()

client.register_handlers_client(dp)
callback.register_handlers_callback(dp)
admin.register_handlers_admin(dp)
extra.register_handlers_extra(dp)
fsmAdminMentor.register_handlers_fsmAdminMentor(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
