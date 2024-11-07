from aiogram import Router, types
from aiogram.filters import Command


router = Router()


@router.message(Command('statr'))
async def start_cmd(message: types.Message):
    await message.answer(
        'Hi, user'
    )