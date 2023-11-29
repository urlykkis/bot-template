import asyncio
import pytest
import pytest_asyncio

from sqlalchemy import event, text
from sqlalchemy.orm import clear_mappers
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.settings.config import load_config
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.core.session import \
    get_async_engine, sa_sessionmaker, get_sync_engine, \
    create_async_engine, make_connection_string


@pytest.fixture(scope="session")
def config():
    return load_config(env_file=".env.test")


@pytest.fixture(scope="session")
def engine(config):
    return get_async_engine(str(config.database.dsn))


@pytest.fixture(scope="session")
def session_factory(config):
    return sa_sessionmaker(str(config.database.dsn), echo=True)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_wipe(engine, db_session, event_loop):
    async with engine.begin() as con:
        await con.run_sync(
            Base.metadata.drop_all
        )
        await con.run_sync(
            Base.metadata.create_all
        )


@pytest.fixture(scope="session")
def db_session(session_factory, config) -> AsyncSession:
    sm = session_factory()
    yield sm


async def wipe_db(db_session, schema: str = "public") -> None:
    async with db_session:
        await db_session.execute(text(f"DROP SCHEMA IF EXISTS {schema} CASCADE;"))
        await db_session.commit()
        await db_session.execute(text(f"CREATE SCHEMA {schema};"))
        await db_session.commit()
