from aiogram import Dispatcher
from aiogram.types import Message, ContentType


async def delete_waste_messages(message: Message):
    # print(message)
    await message.delete()


def register_echo_handler(dp: Dispatcher):
    dp.register_message_handler(delete_waste_messages,
                                content_types=[ContentType.ANY])
