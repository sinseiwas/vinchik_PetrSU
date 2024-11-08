import aiogram
from aiogram import Bot, Dispatcher, F


import os
from dotenv import load_dotenv
import asyncio

from database.models import async_main
from handlers import start, make_form, send_form


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
	await async_main()
	dp.include_routers(start.router, make_form.router, send_form.router)
	
	await dp.start_polling(bot)


if __name__ == "__main__":
	asyncio.run(main())