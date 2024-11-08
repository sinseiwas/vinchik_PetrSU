from aiogram import Router, types
from aiogram.filters import Command

import database.requests as rq

router = Router()


@router.message(Command('start'))
async def start_cmd(message: types.Message):
    
    await rq.set_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )

    await message.answer(
        'Hi, user'
    )