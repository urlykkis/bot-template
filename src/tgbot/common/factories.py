from typing import NamedTuple

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.client.session.aiohttp import AiohttpSession

from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from src.tgbot.routers import register_routers
from src.tgbot.common.middleware.request import RetryRequestMiddleware
from src.infrastructure.settings import Config


class DispatcherStorage(NamedTuple):
    storage: BaseStorage
    events_isolation: BaseEventIsolation


def get_storage(config: Config) -> DispatcherStorage:
    """Создает хранилище для Dispatcher"""
    dp_storage = DispatcherStorage(MemoryStorage(), SimpleEventIsolation())

    if config.misc.use_redis:
        storage = RedisStorage.from_url(
            url=str(config.redis.dsn),
            connection_kwargs={"db": config.redis.db},
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
        dp_storage = DispatcherStorage(storage, storage.create_isolation())

    return dp_storage


def get_dispatcher(
    storage: DispatcherStorage,
    fsm_strategy: FSMStrategy | None = FSMStrategy.CHAT,
        **kwargs
) -> Dispatcher:
    """Создает и настраивает Dispathcer Aiogram"""
    dp = Dispatcher(
        storage=storage.storage,
        fsm_strategy=fsm_strategy,
        events_isolation=storage.events_isolation,
        **kwargs,
    )
    register_routers(dp)
    return dp


def get_bot(config: Config, session: AiohttpSession = AiohttpSession()) -> Bot:
    """Создает и настраивает Bot Aiogram"""
    session.middleware(RetryRequestMiddleware())
    return Bot(
        token=config.telegram_bot.token.get_secret_value(),
        parse_mode=ParseMode.HTML,
        session=session,
    )


async def setup_shutdown_events(dp: Dispatcher, bot: Bot):
    await dp.fsm.storage.close()
    await bot.session.close()
