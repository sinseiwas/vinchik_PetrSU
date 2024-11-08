from aiogram.types import FSInputFile
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery


from database.requests import get_forms_by_user


router = Router()


@router.message(Command('my_form'))
async def send_my_form(message: Message):
    forms = await get_forms_by_user(message.from_user.id)
    
    # Форматируем ответ
    if forms:
        response = ""
        for form in forms:
            response += (
                         f"{form.name or 'Not provided'}, "
                         f"{form.age}\n"
                         f"{form.form_text}\n"
                         )
            photo_path = 'photo/' + form.photo_path

    else:
        response = "No forms found for this user."
    
    photo = FSInputFile(photo_path)

    await message.answer_photo(photo, caption=response)