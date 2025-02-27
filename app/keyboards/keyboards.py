# from aiogram.types import ReplyKeyboardMarkup
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from aiogram.filters.callback_data import CallbackData


class LikeCallbackFactory(CallbackData, prefix="like"):
    is_liked: bool
    user_id: int
    user_like_id: int


class YesCallbackFactory(CallbackData, prefix="likes"):
    is_agree: bool
    user_id: int


def get_like_keyboard(user_id, user_like_id):
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Лайк",
                callback_data=LikeCallbackFactory(
                    is_liked=True,
                    user_id=user_id,
                    user_like_id=user_like_id
                ).pack()
            ),
            types.InlineKeyboardButton(
                text="Дизлайк",
                callback_data=LikeCallbackFactory(
                    is_liked=False,
                    user_id=user_id,
                    user_like_id=user_like_id
                ).pack()
            )
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_yes_not_keyboard(user_id):
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Да",
                callback_data=YesCallbackFactory(
                    is_agree=True,
                    user_id=user_id
                    ).pack()
            ),
            types.InlineKeyboardButton(
                text="Нет",
                callback_data=YesCallbackFactory(
                    is_agree=False,
                    user_id=user_id
                    ).pack()
            ),
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
