from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMINS
from keyboards.klient_kb import submit_markup, cancel_markup, duraction_markup
from database.bot_dp import sql_command_insert


# FSM - Finite State Machine

class FSMAdminMentor(StatesGroup):
    id = State()
    name = State()
    duraction = State()
    age = State()
    # group = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Ты не мой БОСС!")
    else:
        if message.chat.type == "private":
            await FSMAdminMentor.name.set()
            await message.answer('Id please:', reply_markup=cancel_markup)
        else:
            await bot.send_message("pishi v lichke!")


async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = f"@{message.from_user.username}"
        data['id'] = message.text
    await FSMAdminMentor.next()
    await message.answer("What's your name?")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdminMentor.next()
    await message.answer("What's your duraction?", reply_markup=duraction_markup)


async def load_duraction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['duraction'] = message.text
    await FSMAdminMentor.next()
    await message.answer("How old you?", reply_markup=cancel_markup)


async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = int(message.text)
    await FSMAdminMentor.next()
    await message.answer("do you want register?")


# async def load_group(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['group'] = int(message.text)
#     await FSMAdminMentor.next()
#     await message.answer("do you want register?", reply_markup=submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'yes':
        await state.finish()
        await message.answer("все свободен!")
    elif message.text.lower() == 'no':
        await state.finish()
        await message.answer("Отмена!")
    else:
        await message.answer("Нипонял!?")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("Отмена!")


def register_handlers_fsmAdminMentor(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True), state="*")

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_id, state=FSMAdminMentor.id)
    dp.register_message_handler(load_name, state=FSMAdminMentor.name)
    dp.register_message_handler(load_duraction, state=FSMAdminMentor.duraction)
    dp.register_message_handler(load_age, state=FSMAdminMentor.age)
    # dp.register_message_handler(load_group, state=FSMAdminMentor.group)

    dp.register_message_handler(submit, state=FSMAdminMentor.submit)




