import asyncio
import pytest

from tests.fixtures.config_fixtures import db_session, db_wipe, session_factory, engine, config
from tests.fixtures.repo_fixtures import uow, user_service, chat_service, channel_service


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
