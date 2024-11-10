# from aiogram.types import ReplyKeyboardMarkup
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


def get_like_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Лайк", callback_data="1"),
            types.InlineKeyboardButton(text="Дизлайк", callback_data="2")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
