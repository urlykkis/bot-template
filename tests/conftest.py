"""Configuration for pytest."""
import asyncio

import pytest

from src.infrastructure.settings.config import load_config

from .utils.alembic import alembic_config_from_url

config = load_config(env_file=".env.test")


@pytest.fixture()
def alembic_config():
    """Alembic configuration object, bound to temporary database."""
    return alembic_config_from_url(str(config.database.dsn))


@pytest.fixture()
def event_loop():
    """Fixture for event loop."""
    return asyncio.new_event_loop()
