from database.models import async_session
from database.models import *
from sqlalchemy import select, update, delete

async def set_user(tg_id, username, first_name, last_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))


        if not user:
            session.add(User(tg_id=tg_id, 
                            username=username,
                            first_name=first_name,
                            last_name=last_name,
                            is_form=False,
                            is_active=True))
            await session.commit()


async def set_user_form(user_id, name, age, form_text, photo_path=None):
    async with async_session() as session:
        if await session.scalar(select(User).where(User.is_active==True))\
            and not await session.scalar(select(Form).where(Form.user_id==user_id)):
            session.add(Form(user_id=user_id,
                            name=name,
                            age=age,
                            form_text=form_text,
                            photo_path=photo_path))
            await session.commit()



async def get_forms_by_user(user_id):
    async with async_session() as session:
        result = await session.execute(select(Form).filter_by(user_id=user_id))
        forms = result.scalars().all()
        return forms

async def get_tg_id():
    async with async_session() as session:
        user_tg_id = await session.scalars(select(User.tg_id))
    
    return user_tg_id
