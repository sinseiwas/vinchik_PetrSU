from typing import (
    Any,
    Dict,
    Callable,
    Awaitable
)
from aiogram.types import CallbackQuery
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from database.base import get_session
from database.users.crud import get_user


class CallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        print("12345")
        async for session in get_session():
            user = await get_user(session, event.from_user.id)
            if user.form is None:
                await event.message.answer("Вы не заполнили форму")
                return

            data['user'] = user
            data['session'] = session
            await handler(event, data)
