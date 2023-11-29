"""Configuration for integrational tests."""
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


@pytest_asyncio.fixture(scope='function')
async def session(engine: AsyncEngine) -> AsyncSession:
    """Async session fixture.

    :param engine: Bind engine for open session
    """
    async with AsyncSession(bind=engine) as session:
        yield session
