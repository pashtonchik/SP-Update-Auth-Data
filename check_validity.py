import asyncio
import json
import requests
from loader import bot
from settings import *


async def check_validity():
    while True:
        try:
            req_get_auth = requests.get(URL_DJANGO + 'get/binance/cookie/')
            req_bd_data = req_get_auth.json()
            cookie = req_bd_data['cookie_binance'].encode('UTF-8')
            headers = {
                'cookie': cookie,
                'csrftoken': req_bd_data['csrf_binance'],
                'clienttype': 'web',
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            req_auth = requests.post(URL_BINANCE_AUTH, headers=headers)
            print(req_auth.json())

            if not req_auth.json()['success']:
                with open('users.json') as f:
                    d = json.load(f)['users']
                print(d)
                for user in d:
                    try:
                        await bot.send_message(user, 'Необходимо обновить данные авторизации!')
                    except Exception as e:
                        print(e)

            await asyncio.sleep(30)
        except Exception as e:
            print(e)

