import lang
import config

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from database.users.crud import get_form_by_user, like_processing

router = Router()


@router.message(Command('my_form'))
async def send_my_form(message: Message):
    form = await get_form_by_user(message.from_user.id)

    if form:
        response = lang.FORM_MESSAGE.format(
            name=form.name,
            age=form.age,
            form_text=form.form_text
        )

        photo_path = config.PHOTO_FOLDER + form.photo_path
        photo = FSInputFile(photo_path)

        await message.answer_photo(photo, caption=response)
    else:
        await message.answer(lang.NO_FORM_MESSAGE)


@router.message(Command('liked'))
async def show_likes(message: Message):
    result = await like_processing()
    await message.answer(result)
