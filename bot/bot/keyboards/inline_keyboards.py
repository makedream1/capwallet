from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton, WebAppInfo)


def create_inline_kb(row_width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=row_width)
    if args:
        [inline_kb.insert(InlineKeyboardButton(
            text=button,
            callback_data=button)) for button in args]
    if kwargs:
        [inline_kb.insert(InlineKeyboardButton(
            text=text,
            callback_data=button)) for button, text in kwargs.items()]
    return inline_kb


def main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)

    wallet_btn: InlineKeyboardButton = InlineKeyboardButton(
        text='💵 Wallet',
        web_app=WebAppInfo(
            url='https://glowing-halva-16459c.netlify.app'))
    web_portal_btn: InlineKeyboardButton = InlineKeyboardButton(
        text='Cap.Live',
        web_app=WebAppInfo(
            url='https://cap.live'))

    keyboard.add(wallet_btn, web_portal_btn)

    return keyboard
