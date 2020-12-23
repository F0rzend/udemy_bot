import re

from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from app import models
from app.loader import dp
from app.config import UUID4_REGEXP


@dp.message_handler(CommandStart(deep_link=re.compile(f'code__{UUID4_REGEXP}'), encoded=True))
async def confirmed_start(msg: types.Message):
    await msg.answer('Дружище, ты уже зарегестрирован в боте.')


@dp.message_handler(CommandStart(deep_link=re.compile(f'code__{UUID4_REGEXP}'), encoded=True), has_access=False)
async def confirmed_start(msg: types.Message, deep_link: re.Match, user: models.User):
    _, code = deep_link.group(0).split('__')
    if code := await models.ReferralCode.get(code):
        await user.update(
            referral_id=code.user_id,
            code=code.code,
            balance=1000,
        ).apply()
        await msg.answer(f'{user.preview}')
    else:
        await msg.answer(f'Токен не действителен')
