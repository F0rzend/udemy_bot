from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.files import JSONStorage

from gino import Gino

from app import config

db = Gino()

bot = Bot(
    token=config.BOT_TOKEN,
    parse_mode=types.ParseMode.HTML,
)

storage = JSONStorage(config.WORK_PATH / 'app' / 'storage.json')

dp = Dispatcher(
    bot=bot,
    storage=storage,
)

__all__ = (
    "bot",
    "storage",
    "dp",
    "db",
)
