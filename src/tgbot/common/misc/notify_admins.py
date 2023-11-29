from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from src.infrastructure.settings import Config
from src.infrastructure.logging import logger


async def on_startup_notify(bot: Bot, config: Config):
    """Рассылает админам о запуске бота"""
    admins = config.misc.admins + config.misc.owners
    admins_ids = set(admins)
    bot_properties = await bot.me()

    for admin_id in admins_ids:
        try:
            message = ["<b>Bot started.</b>\n",
                       f"<b>Bot ID:</b> {bot_properties.id}",
                       f"<b>Bot Username:</b> {bot_properties.username}"]
            await bot.send_message(admin_id, "\n".join(message))
        except TelegramBadRequest:
            pass
        except Exception as e:
            logger.error(e)
