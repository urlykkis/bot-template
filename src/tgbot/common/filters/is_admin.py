from aiogram.filters.base import Filter
from aiogram.types import Message

from src.infrastructure.settings import Config


class AdminFilter(Filter):
    """Является ли пользователь админом"""
    async def __call__(self, message: Message, config: Config) -> bool:
        admins = config.misc.admins + config.misc.owners
        return message.from_user.id in admins
