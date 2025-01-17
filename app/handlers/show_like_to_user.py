from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from database import crud
from keyboards.keyboards import get_yes_not_keyboard, get_like_keyboard
import lang
import asyncio

import os
import lang
import config

router = Router()


class LikeState(StatesGroup):
    form = State()
    like = State()

@router.message(Command("show_likes"))
async def show_likes(message: Message, state: FSMContext, session: AsyncSession):
    print("show_likes"*10)
    users_liked_id = []
    users_likes_id = await crud.get_likes_to_user(session, message.from_user.id)
    likes_counter = 0
    for user in set(users_likes_id):
        user_likes_id = await crud.get_likes_to_user(session, user)
        if user in users_likes_id:
            users_liked_id.append(user)
            likes_counter += 1
            print(users_liked_id)


    if likes_counter == 0:
        await state.clear()
        return
    else:
        await message.answer(
            f'Вы получили {likes_counter} лайков, хотите посмотреть?',
            reply_markup=get_yes_not_keyboard()
        )

    await state.set_state(LikeState.form)
    users_id = await crud.get_user_id(session)

    if message.from_user.id in users_id:
        users_id.remove(message.from_user.id)

    if not users_id:
        await message.answer("Нет доступных анкет.")
        await state.clear()
        return

    await state.update_data(user_id=message.from_user.id, users_id=users_liked_id, current_index=0)


@router.callback_query(F.data == 'yes')
async def handle_yes_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    users_id = data["users_id"]
    current_index = data["current_index"]

    if current_index >= len(users_id):
        await callback.message.answer(lang.ALL_FORMS_WATCHED)
        await state.clear()
        return
    
    current_user_id = users_id[current_index]
    user_form = await crud.get_form_by_user(session, current_user_id)

    photo_path = os.path.join(config.PHOTO_FOLDER, user_form.photo_path)
    photo = FSInputFile(photo_path)

    response = lang.FORM_MESSAGE.format(
        name=user_form.name,
        age=user_form.age,
        form_text=user_form.form_text
    )

    if not callback.message.photo:
        await asyncio.sleep(0.3)
        await callback.message.delete()
    await callback.message.answer_photo(photo, caption=response, reply_markup=get_like_keyboard())
    await state.update_data(current_index=current_index + 1)
    await state.set_state(LikeState.like)

@router.callback_query(F.data == 'not')
async def handle_not_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("👎")

@router.callback_query(LikeState.like)
async def process_like_dislike(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    users_id = data["users_id"]
    current_index = data["current_index"]
    user_id = users_id[current_index - 1]

    if callback.data == "like":
        username = await crud.get_username(session, user_id)
        await callback.message.answer(
            f"У вас взаимный лайк с пользователем ID @{username}! 🎉"
        )
        await crud.remove_like(
            session,
            callback.from_user.id,
            liked_user_id=user_id)
        await crud.remove_like(
            session,
            user_id,
            liked_user_id=callback.from_user.id)
    else:
        await callback.message.answer("👎")


    await callback.answer()
    await handle_yes_callback(callback, state, session)