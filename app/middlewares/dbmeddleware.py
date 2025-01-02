from typing import (
    Any,
    Dict,
    Callable,
    Awaitable
)
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import TelegramObject
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from database.users.connect import get_session

class DBMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async for session in get_session():
            if not isinstance(session, AsyncSession):
                raise TypeError(f"Expected session to be AsyncSession, got {type(session)}")
            data['session'] = session
            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise