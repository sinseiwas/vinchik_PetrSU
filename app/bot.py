import asyncio
import config

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from database.users.models import async_main

from handlers import start, make_form, send_form, show_users_form, show_like_to_user

bot = Bot(token=config.BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def main():
    await async_main()
    dp.include_routers(
        start.router,
        make_form.router,
        send_form.router,
        show_users_form.router,
        show_like_to_user.router
        )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
