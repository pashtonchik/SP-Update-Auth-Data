from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_main():
    button_google = KeyboardButton(text='Получить Google Authenticator')
    button_post_cookie = KeyboardButton(text='Обновить данные авторизации')
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    main_kb.add(button_google)
    main_kb.add(button_post_cookie)
    return main_kb
