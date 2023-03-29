from aiogram import Dispatcher
from aiogram.types import Message, ContentType, CallbackQuery


async def delete_waste_messages(message: Message):
    # print(message)
    await message.delete()


async def process_callback_delete_message(callback_query: CallbackQuery):
    await callback_query.bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id)

    await callback_query.answer()


def register_echo_handler(dp: Dispatcher):
    dp.register_message_handler(delete_waste_messages,
                                content_types=[ContentType.ANY])
    dp.register_callback_query_handler(process_callback_delete_message,
                                       lambda c: c.data == 'delete_message')
