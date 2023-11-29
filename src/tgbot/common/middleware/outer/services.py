from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)

from aiogram import BaseMiddleware, types

from src.domain.user.usecase import UserService
from src.domain.chat.usecase import ChatService
from src.domain.channel.usecase import ChannelService

from src.tgbot.common.middleware.data import MiddlewareData


class ServicesMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.Update,
            data: MiddlewareData
    ) -> Any:
        """Сервисы для обновления данных"""
        data["user_service"] = UserService(uow=data["uow"])
        data["chat_service"] = ChatService(uow=data["uow"])
        data["channel_service"] = ChannelService(uow=data["uow"])
        return await handler(event, data)
