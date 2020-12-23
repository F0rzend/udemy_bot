from aiogram.dispatcher.filters.state import StatesGroup, State


class InputCodeState(StatesGroup):
    input = State()
