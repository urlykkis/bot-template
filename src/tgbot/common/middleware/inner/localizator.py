from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from fluentogram import TranslatorHub, TranslatorRunner

from src.tgbot.common.middleware.data import MiddlewareData


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: MiddlewareData,
    ) -> Any:
        """Выдает объект интернационализации по языку пользователя"""
        event_user = data["event_from_user"]

        if event_user:
            if data.get("i18n") is not None:
                return await handler(event, data)

            hub: TranslatorHub = data.get('translator_hub')
            # ask database for locale
            i18n: TranslatorRunner = hub.get_translator_by_locale(
                event_user.language_code)

            data['i18n'] = i18n
            return await handler(event, data)

        return await handler(event, data)
