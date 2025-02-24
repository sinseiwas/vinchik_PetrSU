from typing import (
    Any,
    Dict,
    Callable,
    Awaitable
)
from aiogram.types import CallbackQuery
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from database.base import get_session
from database.users.crud import get_user, get_user_id


class CallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        async with get_session() as session:
            user = await get_user(session, event.from_user.id)
            if user.form is None:
                await event.message.answer("Вы не заполнили форму")
                return

            data['user'] = user
            data['session'] = session
            data['users_id'] = await get_user_id(session)
            await handler(event, data)
