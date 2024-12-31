from database.users.models import (
    async_session,
    User,
    Form,
    Like
)
from sqlalchemy import (
    select,
    insert,
    update
)


async def set_user(tg_id, username, first_name, last_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(
                User(
                    tg_id=tg_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    is_form=False,
                    is_active=True
                )
            )
            await session.commit()


async def set_user_form(user_id, name, age, form_text, photo_path=None):
    form = await get_form_by_user(user_id)
    async with async_session() as session:
        if form is None:
            session.add(
                Form(
                    user_id=user_id,
                    name=name,
                    age=age,
                    form_text=form_text,
                    photo_path=photo_path
                )
            )
        else:
            await update_form(user_id, name, age, form_text, photo_path)

        await session.commit()


async def update_form(user_id, name, age, form_text, photo_path=None):
    async with async_session() as session:
        stmt = (
            select(Form)
            .where(Form.user_id == user_id)
        )
        result = await session.execute(stmt)
        form = result.scalar_one_or_none()
        form.name = name
        form.age = age
        form.form_text = form_text
        form.photo_path = photo_path


async def get_user(tg_id: int):
    async with async_session() as session:
        stmt = (
            select(User)
            .where(User.tg_id == tg_id)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user


async def get_form_by_user(user_id):
    async with async_session() as session:
        stmt = (
            select(Form)
            .where(Form.user_id == user_id)
        )
        result = await session.execute(stmt)
        form = result.scalar_one_or_none()
        return form


async def get_tg_id():
    async with async_session() as session:
        user_tg_id = await session.scalars(select(User.tg_id))

    return user_tg_id


async def get_user_id():
    async with async_session() as session:
        result = await session.scalars(select(Form.user_id))

        return result.all()


async def set_user_like(user_id, liked_user_id):
    async with async_session() as session:
        user = await session.scalar(
            select(Like).
            where(Like.user_id == user_id)
            )

        if not user:
            session.add(
                Like(
                    user_id=user_id,
                    liked_user_id=liked_user_id
                )
            )
            await session.commit()


async def add_like(user_id: int, liked_users_id: list()):
    async with async_session() as session:
        stmt = (
            update(Like)
            .where(Like.user_id == user_id)
            .values(liked_user_id=liked_users_id)
        )
        await session.execute(stmt)
        await session.commit()


# async def like_processing(user_id):
#     async with async_session() as session:
#         stmt = select(Like).where(Like.user_id==user_id)
#         result = await session.execute(stmt)
#         liked = result.scalar_one_or_none()

#         if liked:
#             user_like = await session.scalar(
#                 select(User.tg_id)
#                 .where(User.id == liked.user_id)
#                 )

#             user_liked = await session.scalar(
#                 select(User.tg_id)
#                 .where(User.id == liked.liked_user_id)
#                 )

#             user_like_str = (
#                 f"@{user_like}" if user_like
#                 else "Неизвестный пользователь"
#                 )
#             user_liked_str = (f"@{user_liked}" if user_liked
#                               else "Неизвестный пользователь"
#                               )

#             await session.commit()

#             return f"{user_like_str} -> {user_liked_str}"
#         else:
#             return 'lol'
