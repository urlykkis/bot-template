from aiogram.filters.base import Filter
from aiogram.types import Message


class NumberFilter(Filter):
    """Является ли текст числом"""
    async def __call__(self, message: Message) -> dict[str, float] | bool:
        try:
            return {"number": float(message.text)}
        except (ValueError, Exception):
            return False
