import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from database.users.models import User, Form, Like
import config

DATABASE_URL = config.DATABASE_URL

async def init_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Form.metadata.create_all)
        await conn.run_sync(Like.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())