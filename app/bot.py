import asyncio
import config

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from handlers import start, make_form, send_form, show_users_form, show_like_to_user
from middlewares.dbmeddleware import DBMiddleware

bot = Bot(token=config.BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/create_form", description="Создать анкету"),
        BotCommand(command="/my_form", description="Моя форма"),
        BotCommand(command="/watch_forms", description="Смотреть чужие анкеты"),
    ]
    await bot.set_my_commands(commands)

async def main():
    # Регистрация миддлваря для работы с базой данных
    dp.message.middleware(DBMiddleware())
    dp.callback_query.middleware(DBMiddleware())

    dp.include_routers(
        start.router,
        make_form.router,
        send_form.router,
        show_users_form.router,
        show_like_to_user.router
    )

    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())