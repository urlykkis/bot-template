from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)

import time

from aiogram import BaseMiddleware
from aiogram import types
from fluentogram import TranslatorRunner

from src.tgbot.common.middleware.data import MiddlewareData


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, slow_mode_delay=0.5):
        self.user_timeouts = {}
        self.slow_mode_delay = slow_mode_delay
        super(ThrottlingMiddleware, self).__init__()

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.Update,
            data: MiddlewareData
    ) -> Any:
        """Анти-флуд"""
        event_user = data["event_from_user"]

        if event_user:
            user_id = event_user.id
            current_time = time.time()

            last_request_time = self.user_timeouts.get(user_id, 0)
            if current_time - last_request_time < self.slow_mode_delay:
                i18n: TranslatorRunner = data["i18n"]
                await event.reply(i18n.default.wait())
                return

            self.user_timeouts[user_id] = current_time
            return await handler(event, data)

        return await handler(event, data)
