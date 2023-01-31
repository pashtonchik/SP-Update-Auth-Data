import asyncio
import json
import logging
import pyotp
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

from check_validity import check_validity
from loader import dp
from main_kb import kb_main
from settings import URL_DJANGO


class PostCookie(StatesGroup):
    input_cookies = State()
    input_csrf = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)['users']
            if message.from_user.id not in users:
                users.append(message.from_user.id)
        with open('users.json', 'w') as f:
            json.dump({"users": users}, f)
    except Exception as e:
        print(e)
    await message.answer(f"Вечер в хату, {message.from_user.first_name}!", reply_markup=kb_main())


@dp.message_handler(commands=['info'])
async def get_info(message: types.Message):
    try:
        await message.answer("Hello!", reply_markup=kb_main())
    except Exception as e:
        print(e)


@dp.message_handler(text=['Получить Google Authenticator'])
async def get_google_auth(message: types.Message):
    try:
        totp = pyotp.TOTP('IJIHJA5EAC5KBGST')
        google_token_now = totp.now()
        await message.answer(f'`{google_token_now}`', reply_markup=kb_main(), parse_mode='Markdown')
    except Exception as e:
        print(e)



@dp.message_handler(text=['Обновить данные авторизации'])
async def update_auth_data_binance(message: types.Message):
    try:
        await message.answer('Введите новые cookie', reply_markup=kb_main())
        await PostCookie.input_cookies.set()
    except Exception as e:
        print(e)


@dp.message_handler(state=PostCookie.input_cookies)
async def get_cookie(message: types.Message, state=FSMContext):
    try:
        await message.answer('Cookie приняты, введите csrf token', reply_markup=kb_main())
        await PostCookie.input_csrf.set()
        await state.update_data(cookie=message.text)
    except Exception as e:
        print(e)


@dp.message_handler(state=PostCookie.input_csrf)
async def req_with_auth_data(message: types.Message, state=FSMContext):
    try:
        state_data = await state.get_data()
        cookies = state_data['cookie']
        data_req = {
            'cookie_binance': cookies,
            'csrf_binance': message.text
        }
        req_update_cookie = requests.post(URL_DJANGO + 'update/binance/cookie/', json=data_req)
        if req_update_cookie.status_code == 200:
            await message.answer('Данные авторизации успешно отправлены!', reply_markup=kb_main())
        else:
            await message.answer('Ошибка отправки данных на сервер, повторите позже', reply_markup=kb_main())
        await state.finish()
    except Exception as e:
        print(e)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Начать"),
        types.BotCommand("info", "Инструкция по использованию"),
    ])


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    asyncio.create_task(check_validity())


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)