import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from app import models
from app.loader import dp, bot
from app.keyboards.inline import generate_input_code_keyboard, cancel_markup
from app.states import InputCodeState
from app.utils import is_valid_uuid


@dp.message_handler(CommandStart())
async def confirmed_start(msg: types.Message, user: models.User):
    await msg.answer(f'Добрый день, {msg.from_user.get_mention(as_html=True)}\n\n{user.preview}')


@dp.message_handler(CommandStart(), has_access=False)
async def unconfirmed_start(msg: types.Message):
    mk = await generate_input_code_keyboard()
    await msg.answer(f'Чтобы использовать этого бота введите код приглашения, либо пройдите по реферальной ссылке',
                     reply_markup=mk)


@dp.callback_query_handler(text='input_code_callback')
async def input_code(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        'Введите реферальный код или нажмите на кнопку отмены, чтобы прекратить ввод',
        reply_markup=cancel_markup,
    )
    await InputCodeState.first()
    await state.update_data(message_id=call.message.message_id)


@dp.callback_query_handler(state=InputCodeState.input, text='cancel')
async def cancel_input_code(call: types.CallbackQuery, state: FSMContext):
    msg_id = (await state.get_data()).get('message_id')
    await state.finish()
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=msg_id,
        text='Ввод реферального кода отменён',
    )


@dp.message_handler(state=InputCodeState.input, has_access=False)
async def input_code_validate(msg: types.Message, state: FSMContext, user: models.User):
    msg_id = (await state.get_data()).get('message_id')
    if not is_valid_uuid(msg.text):
        await bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=msg_id,
            text='Формат кода неверен, попробуйте ещё раз или нажмите на кнопку отмены, чтобы прекратить ввод',
            reply_markup=cancel_markup,
        )
    elif code := await models.ReferralCode.get(msg.text):
        await state.finish()
        await user.update(balance=1000, referral_id=code.user_id, code=code.code).apply()
        return await bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=msg_id,
            text=f'Введёт вердный реферальный код, принадлежащий пользователю {code.user_id}.\n\n'
            f'{user.preview}',
        )
    else:
        await bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=msg_id,
            text='Код неверный. Попробуйте ещё раз или нажмите на кнопку отмены, чтобы прекратить ввод',
            reply_markup=cancel_markup,
        )

    await msg.delete()
    await asyncio.sleep(3)
    if await dp.current_state(chat=msg.chat.id, user=msg.from_user.id).get_state() == "InputCodeState:input":
        await bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=msg_id,
            text='Введите реферальный код или нажмите на кнопку отмены, чтобы прекратить ввод',
            reply_markup=cancel_markup,
        )
