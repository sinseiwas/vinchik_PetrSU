from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
import database.users.crud as rq
from aiogram.fsm.context import FSMContext
import lang
router = Router()


@router.message(Command("start"))
async def start_cmd(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    await rq.set_user(
        session,
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    print(f"{message.from_user.username} зарегистрировался в боте")

    await message.answer(
        lang.START_MESSAGE
    )
