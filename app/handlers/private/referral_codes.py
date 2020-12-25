from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command

from app import models
from app.loader import dp
from app.keyboards.inline import generate_codes_keyboard, generate_code_keyboard
from app.keyboards.callback_data_types import code_callback, remove_code_callback


@dp.message_handler(Command('get_codes'))
@dp.callback_query_handler(text='get_codes')
async def get_codes_handler(query: Union[types.Message, types.CallbackQuery], user: models.User):
    codes = await models.ReferralCode.query.where(models.ReferralCode.user_id == user.id).gino.all()
    markup = await generate_codes_keyboard(codes)

    if isinstance(query, types.Message):
        await query.answer('Список ваших реферальных кодов:', disable_web_page_preview=True, reply_markup=markup)
    elif isinstance(query, types.CallbackQuery):
        await query.message.edit_text(
            'Список ваших реферальных кодов:', disable_web_page_preview=True, reply_markup=markup
        )


@dp.callback_query_handler(code_callback.filter())
async def code_page_handler(call: types.CallbackQuery, callback_data: dict):
    code = await models.ReferralCode.get(callback_data.get('code'))
    markup = await generate_code_keyboard(code)
    await call.message.edit_text(
        text=f'Реферальный код пользователя {call.from_user.get_mention(as_html=True)}\n\n{await code.preview}',
        disable_web_page_preview=True,
        reply_markup=markup
    )


@dp.callback_query_handler(remove_code_callback.filter())
async def code_remove_handler(call: types.CallbackQuery, callback_data: dict, user: models.User):
    code = await models.ReferralCode.get(callback_data.get('code'))
    await code.delete()
    await get_codes_handler(call, user)
    await call.answer('Реферальный код успешно удалён')


@dp.message_handler(Command('generate_code'))
async def generate_code_handler(msg: types.Message, user: models.User):
    code = await models.ReferralCode.create(user_id=user.id)
    await msg.answer(await code.preview, disable_web_page_preview=True)
