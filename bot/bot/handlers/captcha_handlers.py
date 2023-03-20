from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from bot.db.requests import DbRequests
from bot.keyboards.inline_keyboards import create_inline_kb, main_menu_keyboard
from bot.services.captcha_generator import get_captcha_image_with_buttons
from bot.states.verification import UserVerification


async def process_fail_captcha(callback: CallbackQuery,
                               db_request: DbRequests,
                               state: FSMContext):

    callback.bot.captcha_count -= 1
    captcha_count = callback.bot.captcha_count
    if captcha_count > 0:
        captcha, options = get_captcha_image_with_buttons()
        keyboard = create_inline_kb(2, *options)

        callback.message.bot.data['captcha_key'] = captcha['key']
        await callback.message.edit_media(
            media=InputMediaPhoto(captcha['img']),
            reply_markup=keyboard)

        alert_text = f"Вы неверно разгадали капчу.\
        Попыток осталось: {captcha_count}"
        await callback.answer(
            text=alert_text, show_alert=True)
    else:
        await state.reset_state()
        await db_request.block_user(callback.from_user.id)
        await callback.bot.delete_message(
            callback.message.chat.id, callback.message.message_id)
        await callback.answer('Вы заблокированы!!')

    await callback.answer()


async def process_success_captcha(callback: CallbackQuery,
                                  db_request: DbRequests,
                                  state: FSMContext):
    await state.finish()
    await db_request.verify_user(callback.from_user.id)

    await callback.message.answer_photo(
            photo='AgACAgIAAxkBAAMLZBTIKlatIG4GpBcL-2vpJmU51bYAAmzJMRu4J6lIfcoXKcyWcMoBAAMCAANzAAMvBA',  # noqa: E501
            caption='<a href="https://t.me/cap_live">Ads To Earn Platform</a>\n\n'  # noqa: E501
                    '• Зарабатывай $TON получая рекламу\n'
                    '• Получи тысячи активных пользователей отправив $TON',
            reply_markup=main_menu_keyboard(), parse_mode='HTML')
    await callback.bot.delete_message(
        callback.message.chat.id, callback.message.message_id)
    await callback.answer()


def register_captcha_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        process_fail_captcha,
        lambda btn: btn.data != btn.bot.data.get(
            'captcha_key'),
        state=UserVerification.CaptchaState)
    dp.register_callback_query_handler(
        process_success_captcha,
        lambda btn: btn.data == btn.bot.data.get(
            'captcha_key'),
        state=UserVerification.CaptchaState)
