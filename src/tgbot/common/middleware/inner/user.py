from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)

from aiogram import types, BaseMiddleware

from src.domain.user.usecase import GetUser, RegisterUser
from src.domain.user.dto import UserCreateDTO
from src.domain.user.exceptions import UserNotExists
from src.infrastructure.logging import logger

from src.tgbot.common.middleware.data import MiddlewareData


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.Update,
            data: MiddlewareData
    ) -> Any:
        """
        Проверяет, что пользователь в БД (проверяет актуальность его данных)
        или регистрирует его и выдает обратно
        """
        event_user = data["event_from_user"]
        event_chat = data["event_chat"]

        if event_user and event_chat.type == "private":
            try:
                user = await GetUser(uow=data["uow"])(user_id=event_user.id)
            except UserNotExists:
                user = await RegisterUser(uow=data["uow"])(
                    user=UserCreateDTO(
                        user_id=event_user.id,
                        username=event_user.username,
                        is_premium=bool(event_user.is_premium),
                        first_name=event_user.first_name,
                        last_name=event_user.last_name,
                        language_code=event_user.language_code
                    )
                )
            except Exception as e:
                logger.error(e)
                user = None

            data["user"] = user

        return await handler(event, data)
