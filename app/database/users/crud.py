from database.users.models import (
    async_session,
    User,
    Form,
)
from sqlalchemy import select


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
