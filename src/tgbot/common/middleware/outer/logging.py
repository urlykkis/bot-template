from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.tgbot.common.middleware.data import MiddlewareData
from src.infrastructure.logging import logger


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData
    ) -> Any:
        """Логгирует апдейты бота"""
        logger.debug(event.model_dump())
        return await handler(event, data)
