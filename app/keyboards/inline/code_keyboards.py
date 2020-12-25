from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.models import ReferralCode
from app.keyboards.callback_data_types import code_callback, remove_code_callback


async def generate_input_code_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Ввести код', callback_data='input_code_callback')]
    ])


async def generate_codes_keyboard(codes: List[ReferralCode]) -> InlineKeyboardMarkup:
    mk = InlineKeyboardMarkup(row_width=1)

    for code in codes:
        mk.insert(
            InlineKeyboardButton(
                text=str(code.code),
                callback_data=code_callback.new(code.code)
            )
        )

    return mk


async def generate_code_keyboard(code: ReferralCode) -> InlineKeyboardMarkup:
    mk = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Удалить',
                    callback_data=remove_code_callback.new(code.code),
                )
            ],
            [
                InlineKeyboardButton(
                    text='Список кодов',
                    callback_data='get_codes',
                )
            ]
        ]
    )

    return mk

new_code_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Создать реферальный код',
                callback_data='generate_code'
            )
        ]
    ]
)
