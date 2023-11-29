from aiogram.filters.base import Filter
from aiogram.types import Message

from src.infrastructure.settings import Config


class OwnerFilter(Filter):
    """Является ли пользователь владельцем"""
    async def __call__(self, message: Message, config: Config) -> bool:
        return message.from_user.id in config.misc.owners
