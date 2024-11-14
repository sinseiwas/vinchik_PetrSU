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

    await state.update_data(users_id=users_id, current_index=0)
    await display_form(message, state)


async def display_form(message: Message, state: FSMContext):
    data = await state.get_data()
    users_id = data["users_id"]
    current_index = data["current_index"]

    if current_index < len(users_id):
        user_id = users_id[current_index]
        form = await crud.get_form_by_user(user_id)
        response_text = lang.FORM_MESSAGE.format(
            name=form.name,
            age=form.age,
            form_text=form.form_text
        )
        photo_path = os.path.join(config.PHOTO_FOLDER, form.photo_path)
        photo = FSInputFile(photo_path)

        await state.set_state(LikesState.like)
        await message.answer_photo(
            photo,
            caption=response_text,
            reply_markup=get_like_keyboard())
    else:
        await message.answer("Все анкеты показаны.")
        await state.clear()


@router.callback_query(LikesState.like)
async def process_like_dislike(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users_id = data["users_id"]
    current_index = data["current_index"]
    user_id = users_id[current_index]

    if callback.data == "1":
        await crud.add_like(callback.from_user.id, user_id)

    await state.update_data(current_index=current_index + 1)
    await display_form(callback.message, state)
    await callback.answer()
