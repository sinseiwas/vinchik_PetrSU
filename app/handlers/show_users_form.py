from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from database.users import crud
from keyboards.keyboards import get_like_keyboard

import os
import lang
import config

router = Router()


class LikesState(StatesGroup):
    form = State()
    like = State()


@router.message(Command("find"))
async def start_showing_forms(message: Message, state: FSMContext):
    await state.set_state(LikesState.form)
    users_id = await crud.get_user_id()

    if message.from_user.id in users_id:
        users_id.remove(message.from_user.id)

    if not users_id:
        await message.answer("Нет доступных анкет.")
        await state.clear()
        return

    await state.update_data(users_id=users_id, liked_users_id='', current_index=0)
    await display_form(message, state)


async def display_form(message: Message, state: FSMContext):
    data = await state.get_data()
    users_id = data["users_id"]
    current_index = data["current_index"]

    # Проверка на завершение показа анкет
    if current_index >= len(users_id):
        await crud.set_user_like(message.from_user.id, data["liked_users_id"])
        await crud.add_like(message.from_user.id, data["liked_users_id"])
        await message.answer("Все анкеты показаны.")
        await state.clear()
        return

    user_id = users_id[current_index]
    user_form = await crud.get_form_by_user(user_id)

    photo_path = os.path.join(config.PHOTO_FOLDER, user_form.photo_path)
    photo = FSInputFile(photo_path)

    response = lang.FORM_MESSAGE.format(
        name=user_form.name,
        age=user_form.age,
        form_text=user_form.form_text
    )

    await message.answer_photo(photo, caption=response, reply_markup=get_like_keyboard())
    await state.update_data(current_index=current_index + 1)
    await state.set_state(LikesState.like)


@router.callback_query(LikesState.like)
async def process_like_dislike(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data["current_index"]
    users_id = data["users_id"]
    liked_users_id = data["liked_users_id"]
    liked_users_id += str(users_id[current_index-1]) + " "

    if callback.data == "1":  # Если пользователь поставил "лайк"
        user_id = users_id[current_index - 1]  # Предыдущая анкета
        await state.update_data(liked_users_id=liked_users_id)
        data = await state.get_data()

    await callback.answer()
    await display_form(callback.message, state)
