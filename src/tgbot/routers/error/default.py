from typing import Any

from aiogram import Router
from aiogram.exceptions import (
    TelegramAPIError,
    TelegramUnauthorizedError,
    TelegramBadRequest,
    TelegramNetworkError,
    TelegramNotFound,
    TelegramConflictError,
    TelegramForbiddenError,
    RestartingTelegram,
    CallbackAnswerException,
    TelegramEntityTooLarge,
    TelegramRetryAfter,
    TelegramMigrateToChat,
    TelegramServerError
)
from aiogram.handlers import ErrorHandler

from src.infrastructure.logging import logger

router = Router(name="errors")


@router.errors()
class MyErrorHandler(ErrorHandler):
    async def handle(self, ) -> Any:
        """
        Обработчик ошибок
        :param dispatcher:
        :param update:
        :param exception:
        :return: stdout logger
        """
        if isinstance(self.exception_name, TelegramUnauthorizedError):
            logger.info(f'Unauthorized: {self.exception_message}')
            return True

        if isinstance(self.exception_name, TelegramNetworkError):
            logger.exception(
                f'NetworkError: {self.exception_message} \nUpdate: {self.update}')
            return True

        if isinstance(self.exception_name, TelegramNotFound):
            logger.exception(
                f'NotFound: {self.exception_message} \nUpdate: {self.update}')
            return True

        if isinstance(self.exception_name, TelegramConflictError):
            logger.exception(
                f'ConflictError: {self.exception_message} \nUpdate: {self.update}')
            return True

        if isinstance(self.exception_name, TelegramForbiddenError):
            logger.exception(
                f'ForbiddenError: {self.exception_message} \nUpdate: {self.update}')
            return True

        if isinstance(self.exception_name, CallbackAnswerException):
            logger.exception(
                f'CallbackAnswerException: {self.exception_message} \nUpdate: {self.update}')
            return True

        if isinstance(self.exception_name, TelegramMigrateToChat):
            logger.exception(
                f'BadRequest: {self.exception_message} \nUpdate: {self.update}')
            return True

        if isinstance(self.exception_name, TelegramServerError):
            logger.exception(
                f'BadRequest: {self.exception_message} \nUpdate: {self.update}')
            return True

        if isinstance(self.exception_name, TelegramAPIError):
            logger.exception(
                f'EntityTooLarge: {self.exception_message} \nUpdate: {self.update}')
            return True

        if isinstance(self.exception_name, TelegramRetryAfter):
            logger.exception(
                f'BadRequest: {self.exception_message} \nUpdate: {self.update}')
            return True

        if isinstance(self.exception_name, TelegramEntityTooLarge):
            logger.exception(
                f'EntityTooLarge: {self.exception_message} \nUpdate: {self.update}')
            return True

        if isinstance(self.exception_name, TelegramBadRequest):
            logger.exception(
                f'BadRequest: {self.exception_message} \nUpdate: {self.update}')
            return True

        if isinstance(self.exception_name, RestartingTelegram):
            logger.exception(
                f'Restarting Telegram: {self.exception_message} \nUpdate: {self.update}')
            return True

        logger.exception(f'Update: {self.update} \n{self.exception_name}')
