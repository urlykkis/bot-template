from aiogram.filters.base import Filter
from aiogram.types import Message

from src.domain.user.dto import UserDTO


class RegisterFilter(Filter):
    """Является ли пользователь зарегистрированным"""
    async def __call__(self, message: Message, user: UserDTO | None) -> bool:
        return bool(user)
