from aiogram import Bot, Dispatcher, types, executor
from keys import TOKEN, ADMIN
from database import sqlite as db
from database.state import Register, RC, Fasol, Sinop, Admin
import keyboards.keyboard as kb
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import asyncio
import aioschedule
from datetime import datetime

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    await message.answer(text=f'Привет, {name}\n'
                              f'Я бот, через которого Вам нужно передавать счетчики\n'
                              f'\nЯ напомню, когда это нужно сделать, а так же если Вы это не сделаете ;)')
    user = await db.status(user_id)
    if user:
        await message.answer(text='Вы можете посмотреть прошлые поданные данные:', reply_markup=kb.help())
    else:
        await message.answer(text='Для начала Вам нужно зарегистрироваться:', reply_markup=kb.start())


@dp.callback_query_handler(text='register')
async def register(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer(text='Напишите название вашей компании:')
    await Register.info.set()


@dp.message_handler(state=Register.info)
async def final_register(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['info'] = message.text
    count = data.get('info')
    await message.answer(text='Спасибо за регистрацию, данные сохранены!')
    await bot.send_message(chat_id=ADMIN,
                           text=f'Пользователь USER ID:`{message.from_user.id}`\n {message.from_user.full_name} прислал данные для подтверждения:\n'
                                f'{count}',
                           parse_mode=types.ParseMode.MARKDOWN_V2,
                           reply_markup=kb.appeove())

    await state.finish()


@dp.callback_query_handler(text='approve')
async def admin(callback: types.CallbackQuery):
    await bot.send_message(chat_id=ADMIN, text='Введите ID пользователя (только цифры, без двоеточия):')
    await Admin.user_id.set()


@dp.message_handler(state=Admin.user_id)
async def admin1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text
    await message.answer(text='Выберите наименование в БД:',
                         reply_markup=kb.register())
    await Admin.next()


@dp.callback_query_handler(state=Admin.info)
async def admin2(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['info'] = callback.data
    await callback.message.answer(text='Изменения в БД сохранены!')
    user_id = data.get('user_id')
    await db.register(user_id, data)
    await state.finish()


@dp.callback_query_handler(text='all')
async def view_all(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    user_id = callback.from_user.id
    text = await db.status(user_id)
    test = text[1]
    if test == 'Синопская':
        await callback.message.answer(text=f'Прошлые поданые данные: '
                                           f'\nЭлектричество общее: {text[2]}'
                                           f'\nХВС: {text[5]}'
                                           f'\nГВС: {text[6]}')

    elif test == 'Фасоль' or 'Cтачек':
        await callback.message.answer(text=f'Прошлые поданые данные: '
                                           f'\nЭлектричество дневное: {text[3]}'
                                           f'\nЭлектричество ночное: {text[4]}')

    elif test == 'Римского-Корсакова' or 'Лифляндская':
        await callback.message.answer(text=f'Прошлые поданые данные: '
                                           f'\nЭлектричество общее: {text[2]}')


@dp.callback_query_handler(text='give_count')
async def start_give_counter(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_reply_markup()
    text = await db.status(user_id)
    test = text[1]
    if test == 'Синопская':
        await callback.message.answer(text='Введите Электричество общее:')
        await Sinop.el.set()
    elif test == 'Фасоль' or 'Cтачек':
        await callback.message.answer(text='Введите Электричество дневное:')
        await Fasol.el_d.set()
    elif test == 'Римского-Корсакова' or 'Лифляндская':
        await callback.message.answer(text='Введите Электричество общее:')
        await RC.el.set()


@dp.message_handler(state=RC.el)
async def rc_approve(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    street = await db.cur_status(message)
    async with state.proxy() as data:
        data['el'] = message.text
    cost = data.get('el')
    await message.answer(text='Спасибо! Данные внесены успешно.')
    await bot.send_message(chat_id=ADMIN, text=f'{name} (ул. {street[0]}) подал ЭЛЕКТРИЧЕСТВО ОБЩЕЕ: {cost} ')
    if street[0] == 'Римского-Корсакова':
        await db.approve_RC(message, cost)
        await state.finish()
    else:
        await db.approve_LIF(message, cost)
        await state.finish()


@dp.message_handler(state=Fasol.el_d)
async def fas_step(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['el_d'] = message.text
    await message.answer(text='Введи электричество ночное:')
    await Fasol.next()


@dp.message_handler(state=Fasol.el_n)
async def fas_approve(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    street = await db.cur_status(message)
    async with state.proxy() as data:
        data['el_n'] = message.text
    cost1 = data.get('el_d')
    cost2 = data.get('el_n')
    await message.answer(text='Спасибо! Данные внесены успешно.')
    await bot.send_message(chat_id=ADMIN, text=f'{name} (ул. {street[0]}) подал\n'
                                               f'ЭЛЕКТРИЧЕСТВО ДНЕВНОЕ: {cost1}\n'
                                               f'ЭЛЕКТРИЧЕСТВО НОЧНОЕ: {cost2}')
    if street[0] == 'Фасоль':
        await db.approve_FAS(message, cost1, cost2)
        await state.finish()
    else:
        await db.approve_ST(message, cost1, cost2)
        await state.finish()


@dp.message_handler(state=Sinop.el)
async def sin_step(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['el'] = message.text
    await message.answer(text='ХВС:')
    await Sinop.next()


@dp.message_handler(state=Sinop.hvs)
async def sin_step(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hvs'] = message.text
    await message.answer(text='ГВС:')
    await Sinop.next()


@dp.message_handler(state=Sinop.gvs)
async def fas_approve(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    street = await db.cur_status(message)
    async with state.proxy() as data:
        data['gvs'] = message.text
    cost1 = data.get('el')
    cost2 = data.get('hvs')
    cost3 = data.get('gvs')
    await message.answer(text='Спасибо! Данные внесены успешно.')
    await bot.send_message(chat_id=ADMIN, text=f'{name} (ул. {street[0]}) подал\n'
                                               f'ЭЛЕКТРИЧЕСТВО ОБЩЕЕ: {cost1}\n'
                                               f'ХВС: {cost2}\n'
                                               f'ГВС: {cost3}')

    await db.approve_SIN(message, cost1, cost2, cost3)
    await state.finish()


@dp.message_handler()
async def give_counter():
    users = await db.all_users()
    for user in users:
        while True:
            if datetime.now().strftime("%d %H:%M:%S") == "25 15:00:00":
                await bot.send_message(chat_id=user[0],
                                       text=f'Я напоминаю, пора подавать показатели счетчиков.',
                                       reply_markup=kb.give_count())
                break


async def scheduler():
    asyncio.create_task(give_counter())
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


async def on_startup(_):
    await db.connect()
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
