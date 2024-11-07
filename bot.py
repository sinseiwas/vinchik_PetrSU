import aiogram
from aiogram import Bot, Dispatcher, F


import os
from dotenv import load_dotenv
import asyncio


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
	dp.include_routers()

	await dp.start_polling(bot)


if __name__ == "__name__":
	asyncio.run(main())