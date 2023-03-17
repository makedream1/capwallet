from aiogram import Dispatcher
from aiogram.types import Message


async def delete_waste_messages(message: Message):
    await message.delete()


def register_echo_handler(dp: Dispatcher):
    dp.register_message_handler(delete_waste_messages)
