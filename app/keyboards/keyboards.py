# from aiogram.types import ReplyKeyboardMarkup
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from aiogram.filters.callback_data import CallbackData


class LikeCallbackFactory(CallbackData, prefix="like"):
    is_liked: bool
    user_id: int


def get_like_keyboard(user_id):
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Лайк",
                callback_data=LikeCallbackFactory(
                    is_liked=True,
                    user_id=user_id
                ).pack()
            ),
            types.InlineKeyboardButton(
                text="Дизлайк",
                callback_data=LikeCallbackFactory(
                    is_liked=False,
                    user_id=user_id
                ).pack()
            )
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
