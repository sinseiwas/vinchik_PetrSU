from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession


from database.users import crud
from keyboards.keyboards import (
    get_yes_not_keyboard,
    YesCallbackFactory,
)


router = Router()


async def show_likes(session: AsyncSession, bot: Bot):
    users_id = await crud.get_users_tg_id(session)

    for user_tg_id in users_id:
        user_id = await crud.get_user_id(session, user_tg_id)
        likes_to_user = await crud.get_user_mutual_likes(session, user_id)
        print(likes_to_user)
        if len(likes_to_user) != 0:
            await bot.send_message(
                chat_id=user_tg_id,
                text=f"Ты получил {len(likes_to_user)}\
                      лайков, хочешь посмотреть?",
                reply_markup=get_yes_not_keyboard(user_id)
                )


@router.callback_query(YesCallbackFactory.filter())
async def display_form(
    callback: CallbackQuery,
    callback_data: YesCallbackFactory,
    session: AsyncSession
):
    user_id = callback_data.user_id
    if callback_data.is_agree:
        mutual_likes_ids = await crud.get_user_mutual_likes(session, user_id)
        await callback.message.edit_reply_markup(reply_markup=None)
        print(mutual_likes_ids)

        for user_liked_id in mutual_likes_ids:
            username = await crud.get_username(session, user_liked_id)
            await callback.message.answer(
                f"У тебя взаимный лайк с @{username}"
                )

            await crud.remove_like(
                session,
                user_id,
                liked_user_id=user_liked_id
            )
            await crud.remove_like(
                    session,
                    user_liked_id,
                    liked_user_id=user_id
                )
    else:
        await callback.message.edit_reply_markup(reply_markup=None)

    await callback.answer()
