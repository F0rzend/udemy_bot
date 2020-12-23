from aiogram import Dispatcher
from aiogram.utils import executor

from app import utils, config
from app.loader import dp

# The configuration of the modules using import
from app import middlewares, filters, handlers

from app.models import base, User


async def on_startup(dispatcher: Dispatcher):
    await base.connect(config.POSTGRES_URI)

    await (await User.get(int(config.SUPERUSER_IDS[0]))).update(is_superuser=False, code=None, referral_id=None).apply()

    await utils.setup_default_commands(dispatcher)
    await utils.notify_admins(config.SUPERUSER_IDS)


async def on_shutdown(dispatcher: Dispatcher):
    await base.close_connection()


if __name__ == '__main__':
    utils.setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])
    executor.start_polling(
        dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=config.SKIP_UPDATES
    )
