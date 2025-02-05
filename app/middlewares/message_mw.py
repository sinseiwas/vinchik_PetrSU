from aiogram.dispatcher.middlewares.base import BaseMiddleware
from database.base import get_session
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import Message


class SessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        async for session in get_session():
            data["session"] = session
            await handler(event, data)
