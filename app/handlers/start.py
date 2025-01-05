from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
import database.crud as rq
from handlers.show_like_to_user import show_likes
from aiogram.fsm.context import FSMContext

import lang
router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext, session: AsyncSession):
    await rq.set_user(
        session,
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await message.answer(
        lang.START_MESSAGE
    )

    await show_likes(message, state, session)
