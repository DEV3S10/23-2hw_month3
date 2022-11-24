import random
import sqlite3
from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных подключена!")

    db.execute("CREATE TABLE IF NOT EXISTS anketa "
               "(username TEXT, id INTEGER, name TEXT, duraction TEXT, "
               "age INTEGER)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO anketa VALUES "
                       "(?, ?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM anketa").fetchall()
    random_user = random.choice(result)
    await bot.send_photo(message.from_user.id, random_user[6],
                         caption=f"{random_user[2]} {random_user[3]} {random_user[4]} "
                                 f"{random_user[5]}\n{random_user[1]}")


async def sql_command_all() -> list:
    return cursor.execute("SELECT * FROM anketa").fetchall()


async def sql_command_delete(user_id) -> None:
    cursor.execute("DELETE FROM anketa WHERE id = ?", (id,))
    db.commit()


async def sql_command_get_all_ids() -> list:
    return cursor.execute("SELECT id FROM anketa").fetchall()
