from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from database.users import crud
from keyboards.keyboards import get_yes_not_keyboard, get_like_keyboard


import os
import lang
import config

router = Router()


class LikeState(StatesGroup):
    form = State()
    like = State()


@router.message(Command('i_liked'))
async def show_likes(message: Message, state: FSMContext):
    users_liked_id = []
    users_likes_id = await crud.get_likes_to_user(message.from_user.id)
    likes_counter = 0
    for user in set(users_likes_id):
        user_likes_id = await crud.get_likes_to_user(user)
        if user in users_likes_id:
            users_liked_id.append(user)
            likes_counter += 1

    if likes_counter == 0:
        print('User have no likes')
        return 0
    else:
        await message.answer(
            f'Вы получили {likes_counter} лайков, хотите посмотреть?',
            reply_markup=get_yes_not_keyboard()
            )

    await state.set_state(LikeState.form)
    users_id = await crud.get_user_id()

    if message.from_user.id in users_id:
        users_id.remove(message.from_user.id)

    if not users_id:
        await message.answer("Нет доступных анкет.")
        await state.clear()
        return

    await state.update_data(user_id=message.from_user.id, users_id=users_liked_id, current_index=0)


@router.callback_query(F.data == 'yes')
async def handle_yes_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users_id = data["users_id"]
    current_index = data["current_index"]

    if current_index >= len(users_id):
        await callback_query.message.answer("Все анкеты показаны.")
        await state.clear()
        return

    current_user_id = users_id[current_index]
    user_form = await crud.get_form_by_user(current_user_id)

    photo_path = os.path.join(config.PHOTO_FOLDER, user_form.photo_path)
    photo = FSInputFile(photo_path)

    response = lang.FORM_MESSAGE.format(
        name=user_form.name,
        age=user_form.age,
        form_text=user_form.form_text
    )

    await callback_query.message.answer_photo(photo, caption=response, reply_markup=get_like_keyboard())
    await state.update_data(current_index=current_index + 1)
    await state.set_state(LikeState.like)


@router.callback_query(LikeState.like)
async def process_like_dislike(callback: CallbackQuery, state: FSMContext):
    if callback.data == "like":
        await callback.message.answer(
            f"У вас взаимный лайк с пользователем ID @{callback.from_user.username}! 🎉"
        )

    await callback.answer()
    await handle_yes_callback(callback, state)
