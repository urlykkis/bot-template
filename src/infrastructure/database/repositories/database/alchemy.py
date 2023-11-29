from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (select, func)

from src.infrastructure.database.models import Base
from src.infrastructure.database.repositories.database.base \
    import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    """Репозиторий для работы с SQLAlchemy"""
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def _set_one(self, obj: Base):
        self.session.add(obj)
        return True

    async def _add_one(self, model: Base) -> Base:
        await self._set_one(model)
        return model

    async def count(self, model: Base) -> int:
        stmt = select(func.count(model))
        return await self.session.scalar(stmt)
