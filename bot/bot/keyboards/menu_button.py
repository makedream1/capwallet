from aiogram import Dispatcher, types
from aiogram.types.bot_command_scope import BotCommandScopeDefault


async def set_main_menu(dp: Dispatcher):
    main_menu_commands = [
        types.BotCommand(command='/start',
                         description='Меню'),
    ]
    await dp.bot.set_my_commands(
        main_menu_commands, scope=BotCommandScopeDefault())
