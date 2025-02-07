import asyncio
import config
import sys
import os
import database
import logging
from database import base
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from handlers import (
    start,
    make_form,
    send_form,
    show_users_form,
    show_like_to_user
)
from middlewares.callback_mw import CallbackMiddleware
from middlewares.message_mw import SessionMiddleware


bot = Bot(token=config.BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/create_form", description="Создать анкету"),
        BotCommand(command="/my_form", description="Моя анкета"),
        BotCommand(
            command="/watch_forms",
            description="Смотреть чужие анкеты"
            ),
    ]
    await bot.set_my_commands(commands)


async def periodic_task(interval: int):
    while True:
        async with base.get_session() as session:
            await show_like_to_user.show_likes(session)
        await asyncio.sleep(interval)


async def main():
    if not os.path.exists(config.DATABASE_URL):
        await database.init_db()

    if "reload" in sys.argv:
        await database.init_db()

    dp.message.middleware(SessionMiddleware())
    dp.callback_query.middleware(CallbackMiddleware())

    dp.include_routers(
        start.router,
        make_form.router,
        send_form.router,
        show_users_form.router,
        show_like_to_user.router
    )

    # asyncio.create_task(periodic_task(3600))
    await set_commands(bot)
    logging.info("Start polling")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
