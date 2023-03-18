from aiogram import Dispatcher
from aiogram.types import Message

from bot.db.requests import DbRequests
from bot.keyboards.inline_keyboards import create_inline_kb, main_menu_keyboard
from bot.services.captcha_generator import get_captcha_image_with_buttons
from bot.states.verification import UserVerification


async def process_start(message: Message,
                        db_request: DbRequests):
    user = await db_request.get_user(user_id=message.from_user.id)
    if not user.is_active:
        await message.answer('Вы заблокированы!!')
    elif not user.is_verified:
        captcha, options = get_captcha_image_with_buttons()
        keyboard = create_inline_kb(2, *options)
        message.bot.captcha_count = 3
        message.bot.data['captcha_key'] = captcha['key']
        await message.answer_photo(photo=captcha['img'],
                                   caption='Пожалуйста, решите капчу',
                                   reply_markup=keyboard)
        await UserVerification.CaptchaState.set()
    else:
        await message.answer_photo(
            photo='AgACAgIAAxkBAAMLZBTIKlatIG4GpBcL-2vpJmU51bYAAmzJMRu4J6lIfcoXKcyWcMoBAAMCAANzAAMvBA',  # noqa: E501
            caption='Мультивалютный криптокошелек. Покупайте, продавайте, храните и платите криптовалютой когда хотите.',  # noqa: E501
            reply_markup=main_menu_keyboard())
    await message.delete()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(
        process_start, commands='start', state="*")
