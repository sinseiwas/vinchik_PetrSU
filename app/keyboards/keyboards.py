# from aiogram.types import ReplyKeyboardMarkup
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


def get_like_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Лайк", callback_data="like"),
            types.InlineKeyboardButton(text="Дизлайк", callback_data="dislike")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_yes_not_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Да", callback_data="yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="not")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard