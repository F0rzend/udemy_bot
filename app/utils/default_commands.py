from aiogram import types
from loguru import logger


async def setup_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "start"),
            types.BotCommand("get_codes", "get all your referral codes"),
            types.BotCommand("generate_code", "generate new referral code"),
        ]
    )
    logger.info('Standard commands are successfully configured')
