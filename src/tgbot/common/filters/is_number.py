from aiogram.filters.base import Filter
from aiogram.types import Message


class NumberFilter(Filter):
    """Является ли текст числом"""
    async def __call__(self, message: Message) -> bool:
        try:
            float(message.text)
            return True
        except (ValueError, Exception):
            return False
