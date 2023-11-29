from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)

from datetime import datetime, timedelta

from aiogram import BaseMiddleware, types
from aiogram.fsm.context import FSMContext

from src.infrastructure.settings import Config
from src.infrastructure.logging import logger

from src.tgbot.common.middleware.data import MiddlewareData


class GlobalTimeoutMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.Update,
            data: MiddlewareData,
    ) -> Any:
        """
        Проверяет, на общий таймаут у юзера
        """
        event_user = data["event_from_user"]

        if event_user:
            config: Config = data["config"]
            state: FSMContext = data["state"]
            i18n = data["i18n"]
            state_data = await state.get_data()
            global_timeout = state_data.get("global_timeout")

            if not global_timeout:
                return await handler(event, data)

            global_timeout = datetime.strptime(
                global_timeout, "%Y-%m-%d %H:%M:%S.%f"
            )

            until = global_timeout + timedelta(seconds=config.misc.global_timeout)

            if until <= datetime.now():
                await state.update_data(global_timeout=None)
                return await handler(event, data)

            timeout = (until - datetime.now()).seconds

            logger.warning(
                f"GlobalTimeoutMiddleware -> User: {event_user.id} is on global timeout ({timeout}s left)."
            )
            await event.answer(i18n.timeout())
            return False

        return await handler(event, data)
