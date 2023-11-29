from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    """Основа для репозиториев"""
    def __init__(self, session: AsyncSession):
        self.session = session
