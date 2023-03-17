from aiogram.dispatcher.filters.state import StatesGroup, State


class UserVerification(StatesGroup):
    CaptchaState = State()
