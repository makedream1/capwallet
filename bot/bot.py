import asyncio
import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.engine import URL

from bot.config import Config, load_config
from bot.db.base import BaseModel
from bot.db.engine import (async_session_generator,
                           create_async_engine, proceed_schemas)
from bot.handlers.other_handlers import register_echo_handler
from bot.handlers.user_handlers import register_user_handlers
from bot.handlers.captcha_handlers import register_captcha_handlers
from bot.keyboards.menu_button import set_main_menu
from bot.middlewares.db import DbMiddleware
from bot.middlewares.ton_mw import TONMiddleware
from bot.tasks.ton_task import ton_deposit_watcher, ton_withdraw_watcher
from bot.tasks.update_prices_task import update_prices


logger = logging.getLogger(__name__)


def register_all_handlers(dp: Dispatcher) -> None:
    register_user_handlers(dp)
    register_captcha_handlers(dp)
    register_echo_handler(dp)


async def main() -> None:
    logger.info('Starting bot')

    config: Config = load_config('.env')

    if config.bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()

    engine = create_async_engine(URL.create(
        'postgresql+asyncpg',
        username=config.db.db_user,
        password=config.db.db_password,
        host=config.db.db_host,
        database=config.db.database
    ))
    await proceed_schemas(engine, BaseModel.metadata)
    async_session = async_session_generator(engine)

    bot = Bot(config.bot.token, parse_mode=types.ParseMode.HTML)
    bot['captcha_count'] = 3
    dp = Dispatcher(bot, storage=storage)

    dp.middleware.setup(DbMiddleware(async_session))
    register_all_handlers(dp)

    if config.ton.TESTNET:
        TONCENTER_API_KEY = config.ton.API_KEY_TESTNET
    else:
        TONCENTER_API_KEY = config.ton.API_KEY_MAINNET

    dp.middleware.setup(TONMiddleware(TONCENTER_API_KEY, config.ton.TESTNET))

    await set_main_menu(dp)

    try:
        asyncio.gather(ton_deposit_watcher(config, async_session),
                       ton_withdraw_watcher(config, async_session),
                       update_prices(config, async_session))

        executor.start_polling(dp)
    finally:
        async with async_session() as session:
            await session.close()
        session = await bot.get_session()
        await session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
