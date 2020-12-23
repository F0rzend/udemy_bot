from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
    ]
)
