import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")


logging.basicConfig(level=logging.INFO)
bot = Bot(token="5830847125:AAEL3vbrU0fvdEsvZmA2crtBPwpjjhA6Ob0")
dp = Dispatcher(bot=bot, storage=MemoryStorage())