from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (select, func)
from datetime import datetime

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

    async def count_model(self, model) -> int:
        stmt = select(func.count()).select_from(model)
        return await self.session.scalar(stmt)

    async def count_model_by_time(self, model, time):
        now = datetime.now().replace(microsecond=0)
        stmt = select(func.count())\
            .select_from(model)\
            .filter(model.created_at >= time, model.created_at <= now)

        result = await self.session.scalar(stmt)
        return 0 if result is None or not result else result
