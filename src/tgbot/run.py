import asyncio

from typing import Never

from aiohttp import web
from aiogram import Bot
from apscheduler.triggers.cron import CronTrigger
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, \
    setup_application

from src.domain.enums.log_level import LogLevel

from src.infrastructure.settings.config import Config
from src.infrastructure.database.core.session import sa_sessionmaker
from src.infrastructure.settings.config import load_config
from src.infrastructure.logging import setup_logger, logger
from src.infrastructure.i18n import translator_hub
from src.infrastructure.scheduler.apschedule import get_scheduler

from src.tgbot.common.middleware import register_middleware
from src.tgbot.common.misc.set_my_commands import set_bot_commands
from src.tgbot.common.misc.notify_admins import on_startup_notify
from src.tgbot.common.misc.jobs.autobackup import auto_backup

from src.tgbot.common.factories import \
    get_dispatcher, get_bot, \
    get_storage, setup_shutdown_events


async def set_webhook(bot: Bot, config: Config) -> None:
    webhook_path = f"{config.web.WEBHOOK_URL}{config.web.WEBHOOK_PATH}"
    logger.debug(f"Webhook PATH: {webhook_path}")
    await bot.set_webhook(webhook_path)


def default_setup():
    setup_logger(LogLevel.DEBUG.value, ["aiogram.bot.api"])
    config = load_config()

    bot = get_bot(config=config)
    storage = get_storage(config=config)
    dp = get_dispatcher(storage=storage)
    database = sa_sessionmaker(str(config.database.dsn))

    register_middleware(dp=dp, sm=database)

    return bot, dp, storage, config, database


async def run_bot_polling() -> Never:
    """Запуск бота"""
    bot, dp, storage, config, database = default_setup()

    scheduler = await get_scheduler(config=config)

    async with scheduler:
        await scheduler.add_schedule(
            func_or_task_id=auto_backup,
            trigger=CronTrigger(hour=0),
            id="autobackup_1",
            args=(bot, config, database),
        )
        await scheduler.start_in_background()

    try:
        await set_bot_commands(bot=bot, config=config)

        if config.misc.notify_admins:
            await on_startup_notify(bot=bot, config=config)

        await bot.delete_webhook()
        await bot.get_updates(offset=-1)
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            config=config,
            translator_hub=translator_hub,
        )
    except RuntimeError:
        await setup_shutdown_events(dp=dp, bot=bot)


def run_bot_webhook():
    bot, dp, storage, config, database = default_setup()

    dp.startup.register(set_webhook)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=config.web.WEBHOOK_PATH)

    dp.workflow_data.update(
        translator_hub=translator_hub, config=config,
        database=database
    )

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=config.web.HOST, port=config.web.PORT)


if __name__ == "__main__":
    asyncio.run(run_bot_polling())
