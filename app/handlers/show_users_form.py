from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from database.users import crud
# from database.users.models import User
from keyboards.keyboards import get_like_keyboard, LikeCallbackFactory

import os
import lang
import config


router = Router()


@router.message(Command("watch_forms"))
async def start_showing_forms(
    message: Message,
    # user: User,
    session: AsyncSession
):
    user_id = await crud.get_user_id(session, message.from_user.id)

    await display_form(message, session, user_id)


async def display_form(
        message: Message,
        session: AsyncSession,
        user_id,
):
    user_like_id = await crud.get_random_user_id(session, user_id)

    if not user_like_id:
        await message.answer(lang.ALL_FORMS_WATCHED)
        return

    user_form = await crud.get_form_by_user(session, user_like_id)

    photo_path = os.path.join(config.PHOTO_FOLDER, user_form.photo_path)
    photo = FSInputFile(photo_path)

    response = lang.FORM_MESSAGE.format(
        name=user_form.name,
        age=user_form.age,
        form_text=user_form.form_text
    )
    print(user_form.age, user_form.name, user_form.form_text, user_like_id)

    await message.answer_photo(
        photo=photo,
        caption=response,
        reply_markup=get_like_keyboard(user_id, user_like_id)
        )


@router.callback_query(LikeCallbackFactory.filter())
async def process_like_dislike(
    callback: CallbackQuery,
    callback_data: LikeCallbackFactory,
    session: AsyncSession,
):
    liked_user_id = callback_data.user_like_id
    user_id = await crud.get_user_id(session, callback.from_user.id)

    if callback_data.is_liked:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("👍")
        await crud.add_like(session, user_id, liked_user_id)
    else:
        await crud.add_dislike(session, user_id, liked_user_id)
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("👎")

    await callback.answer()
    await display_form(callback.message, session, user_id)
