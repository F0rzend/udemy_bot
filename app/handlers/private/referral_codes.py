from aiogram import types
from aiogram.dispatcher.filters import Command

from app import models
from app.loader import dp


@dp.message_handler(Command('get_codes'))
async def get_codes_handler(msg: types.Message, user: models.User):
    codes = '\n'.join(
        [f'{index + 1}) {await code.preview}' for index, code in enumerate(
            await models.ReferralCode.query.where(models.ReferralCode.user_id == user.id).gino.all()
        )]
    )
    text = 'Список ваших реферальных кодов:\n' + codes
    await msg.answer(text, disable_web_page_preview=True)


@dp.message_handler(Command('generate_code'))
async def get_codes_handler(msg: types.Message, user: models.User):
    code = await models.ReferralCode.create(user_id=user.id)
    await msg.answer(await code.preview, disable_web_page_preview=True)
