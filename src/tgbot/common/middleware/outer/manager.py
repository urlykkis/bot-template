from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.tgbot.common.middleware.data import MiddlewareData


class ManagerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData
    ) -> Any:
        """Bot для использования в обработчиках"""
        data['bot'] = event.bot
        return await handler(event, data)
