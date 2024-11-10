import os
import config

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

from bot import bot

from database.users.crud import set_user_form

router = Router()


class Form(StatesGroup):
    name = State()
    age = State()
    form_text = State()
    photo = State()


@router.message(Command('form'))
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
    await state.update_data(age=message.text)
    await state.set_state(Form.form_text)
    await message.answer('Введите текст анкеты:')


@router.message(Form.form_text)
async def get_form_text(message: Message, state: FSMContext):
    await state.update_data(form_text=message.text)
    await state.set_state(Form.photo)
    await message.answer('Отправьте фото, которое будет отображаться в анкете')


@router.message(Form.photo)
async def get_form_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_name = f"{message.from_user.id}.jpg"
    print(config.PHOTO_FOLDER)
    await bot.download(
        photo.file_id,
        destination=os.path.join(config.PHOTO_FOLDER, file_name)
    )

    await state.update_data(photo=file_name)
    data = await state.get_data()
    await set_user_form(
        user_id=message.from_user.id,
        name=data['name'],
        age=data['age'],
        form_text=data['form_text'],
        photo_path=data['photo']
    )
    await state.clear()
    await message.answer(f"Фото сохранено и анкета завершена. {data}")
