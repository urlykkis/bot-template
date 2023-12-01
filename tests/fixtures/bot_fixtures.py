import pytest
import pytest_asyncio

from tests.mocks.aiogram_mocks.mocked_bot import MockedBot
from src.tgbot.common.factories import get_dispatcher, get_storage

from src.infrastructure.database.core.session import sa_sessionmaker
from src.tgbot.common.middleware import register_middleware

@pytest_asyncio.fixture(scope="session")
async def memory_storage(config):
    return get_storage(config)


@pytest.fixture(scope="session")
def bot(config):
    return MockedBot()


@pytest_asyncio.fixture(scope="session")
async def dispatcher(bot, config, memory_storage, translator_hub):
    dp = get_dispatcher(
        storage=memory_storage, translator_hub=translator_hub,
        bot=bot, config=config,
    )
    database = sa_sessionmaker(str(config.database.dsn))
    register_middleware(dp=dp, sm=database, ignore_throttling=True)

    await dp.emit_startup()

    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest_asyncio.fixture(scope="class")
async def cls_dp(request, dispatcher):
    request.cls.dispatcher = dispatcher

@pytest_asyncio.fixture(scope="class")
async def cls_bot(request, bot):
    request.cls.bot = bot
