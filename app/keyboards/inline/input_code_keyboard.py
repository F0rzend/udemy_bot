from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_input_code_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Ввести код', callback_data='input_code_callback')]
    ])
