from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from database.users.models import User, Like, Form



async def set_user(session: AsyncSession, tg_id, username, first_name, last_name):
    if not isinstance(session, AsyncSession):
        raise TypeError(f"Expected session to be AsyncSession, got {type(session)}")
    
    # Проверка на существование пользователя
    stmt = select(User).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user:
        # Обновление данных пользователя
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
    else:
        # Вставка нового пользователя
        new_user = User(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_form=False,
            is_active=True
        )
        session.add(new_user)


async def set_user_form(session: AsyncSession, user_id, name, age, form_text, photo_path=None):
    form = await get_form_by_user(session, user_id)
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
        await update_form(session, user_id, name, age, form_text, photo_path)


async def update_form(session: AsyncSession, user_id, name, age, form_text, photo_path=None):
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


async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

async def get_user(session: AsyncSession, tg_id: int):
    stmt = (
        select(User)
        .where(User.tg_id == tg_id)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def get_form_by_user(session: AsyncSession, user_id):
    stmt = (
        select(Form)
        .where(Form.user_id == user_id)
    )
    result = await session.execute(stmt)
    form = result.scalar_one_or_none()
    return form


async def get_tg_id(session: AsyncSession):
    user_tg_id = await session.scalars(select(User.tg_id))
    return user_tg_id


async def get_user_id(session: AsyncSession):
    result = await session.scalars(select(Form.user_id))
    return result.all()


async def add_like(session: AsyncSession, user_id: int, liked_user_id: int):
    result = await session.execute(
        select(Like).where(Like.user_id == user_id, Like.liked_user_id == liked_user_id)
    )
    existing_like = result.scalars().first()

    if existing_like is None:
        new_like = Like(user_id=user_id, liked_user_id=liked_user_id)
        session.add(new_like)
        await session.commit()
        print(f"Лайк добавлен: {user_id} -> {liked_user_id}")
    else:
        print(f"Лайк уже существует: {user_id} -> {liked_user_id}")


async def remove_like(session: AsyncSession, user_id: int, liked_user_id: int):
    result = await session.execute(
        select(Like).where(Like.user_id == liked_user_id, Like.liked_user_id == user_id)
    )
    existing_like = result.scalars().first()

    if existing_like:
        await session.delete(existing_like)
        await session.commit()
        print(f"Лайк удален: {liked_user_id} -> {user_id}")
    else:
        print(f"Взаимный лайк не найден: {liked_user_id} -> {user_id}")


async def get_likes_to_user(session: AsyncSession, user_id):
    stmt = (
        select(Like.user_id)
        .where(Like.liked_user_id == user_id)
    )
    result = await session.execute(stmt)
    likes = result.scalars().all()
    return likes


async def get_username(session: AsyncSession, user_id):
    stmt = (
        select(User.username)
        .where(User.tg_id == user_id)
    )
    result = await session.execute(stmt)
    user = result.scalars().one()
    return user
