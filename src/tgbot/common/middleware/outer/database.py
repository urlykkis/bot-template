from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)

from aiogram import BaseMiddleware
from aiogram import types
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.uow import SQLAlchemyUoW
from src.infrastructure.database.repositories.user import UserRepository
from src.infrastructure.database.repositories.chat import ChatRepository
from src.infrastructure.database.repositories.channel import ChannelRepository

from src.tgbot.common.middleware.data import MiddlewareData


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, sm: sessionmaker):
        self.sm: sessionmaker = sm

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: MiddlewareData
    ) -> Any:
        """Создает сессию БД"""
        async with self.sm() as session:
            data["session"] = session
            data["uow"] = SQLAlchemyUoW(
                session=session,
                user_repo=UserRepository,
                chat_repo=ChatRepository,
                channel_repo=ChannelRepository,
            )
            return await handler(event, data)
