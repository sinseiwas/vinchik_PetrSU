import os
import config

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession

from database.users.crud import set_user_form, get_user_from_id

router = Router()


class Form(StatesGroup):
    name = State()
    age = State()
    form_text = State()
    photo = State()


@router.message(Command('create_form'))
async def start_form(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer('Введите ваше имя:')


@router.message(Form.name)
async def get_form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer('Введите ваш возраст:')


@router.message(Form.age)
async def get_form_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        age = int(message.text)
        await state.update_data(age=age)
        await state.set_state(Form.form_text)
        await message.answer('Введите текст анкеты:')
    else:
        await message.answer('Введите числовое значение')


@router.message(Form.form_text)
async def get_form_text(message: Message, state: FSMContext):
    await state.update_data(form_text=message.text)
    await state.set_state(Form.photo)
    await message.answer('Отправьте фото, которое будет отображаться в анкете')


@router.message(Form.photo)
async def get_form_photo(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    photo_folder = config.PHOTO_FOLDER

    if not os.path.exists(photo_folder):
        os.makedirs(photo_folder)

    photo = message.photo[-1]
    file_name = f"{message.from_user.id}.jpg"

    await message.bot.download(
        photo.file_id,
        destination=os.path.join(photo_folder, file_name)
    )

    await state.update_data(photo=file_name)
    data = await state.get_data()

    await set_user_form(
        session,
        user_id=await get_user_from_id(session, message.from_user.id),
        name=data['name'],
        age=data['age'],
        form_text=data['form_text'],
        photo_path=data['photo']
    )

    await message.answer("Фото сохранено и анкета завершена.")

    await state.clear()
