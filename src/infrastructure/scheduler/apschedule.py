from apscheduler import AsyncScheduler
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore

from src.infrastructure.settings.config import Config
from src.infrastructure.database.core.session import create_async_engine


async def get_scheduler(config: Config) -> AsyncScheduler:
    """Планировщик задач"""
    # engine = create_async_engine(str(config.database.dsn))
    # data_store = SQLAlchemyDataStore(engine=engine)

    scheduler = AsyncScheduler()
    return scheduler
