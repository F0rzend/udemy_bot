from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink

from app import models
from app.loader import dp, db
from app.keyboards.inline import generate_codes_keyboard, generate_code_keyboard, new_code_markup
from app.keyboards.callback_data_types import code_callback, remove_code_callback
from app.utils import declension_token


@dp.message_handler(Command('get_codes'))
@dp.callback_query_handler(text='get_codes')
async def get_codes_handler(query: Union[types.Message, types.CallbackQuery], user: models.User):
    codes = await models.ReferralCode.query.where(models.ReferralCode.user_id == user.id).gino.all()
    if not codes:
        if isinstance(query, types.Message):
            return await query.answer('У вас нет реферальных кодов', disable_web_page_preview=True,
                                      reply_markup=new_code_markup)
        elif isinstance(query, types.CallbackQuery):
            return await query.message.edit_text(
                'У вас не осталось реферальных кодов', disable_web_page_preview=True, reply_markup=new_code_markup
            )

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

    code_users = [
        hlink(title=f"ID:{row[0]}", url=f"tg://user?id={row[0]}") for row in
        await models.User.select('id').where(models.User.code == code.code).gino.all()
    ]

    text = '\n'.join([
        f'Реферальный код',
        await code.preview,
        f'\nПользователи, зарегестрированные по этому коду({len(code_users)})',
    ] + code_users or [])
    markup = await generate_code_keyboard(code)
    await call.message.edit_text(
        text=text,
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
@dp.callback_query_handler(text='generate_code')
async def generate_code_handler(query: Union[types.Message, types.CallbackQuery], user: models.User):
    count = await db.select(
        [db.func.count(models.ReferralCode.user_id)]
    ).select_from(models.ReferralCode).where(models.ReferralCode.user_id == user.id).gino.scalar()

    if count <= 5 or user.is_superuser:
        code = await models.ReferralCode.create(user_id=user.id)
        text = f'Теперь у вас {count + 1} {declension_token(count + 1)}\n\nТокен успешно создан:\n{await code.preview}'
        markup = await generate_code_keyboard(code)
        if isinstance(query, types.Message):
            await query.answer(text, disable_web_page_preview=True, reply_markup=markup)
        elif isinstance(query, types.CallbackQuery):
            await query.message.edit_text(text, disable_web_page_preview=True, reply_markup=markup)
    else:
        await query.answer(
            'Вы не можете создать больше пяти реферальных кодов. Пожалуйста используйте уже существующий код'
        )
