from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, \
    BotCommandScopeAllPrivateChats, \
    BotCommandScopeAllGroupChats, \
    BotCommandScopeAllChatAdministrators
from aiogram.exceptions import TelegramBadRequest

from src.infrastructure.settings import Config
from src.infrastructure.logging import logger


async def set_bot_commands(bot: Bot, config: Config):
    """Устанавливает команды бота"""
    user_commands: list[BotCommand] = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь по боту"),
        BotCommand(command="settings", description="Настройки"),
    ]

    chat_commands: list[BotCommand] = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь по боту"),
    ]

    admin_chat_commands: list[BotCommand] = chat_commands + [
    ]

    admins_commands: list[BotCommand] = [
        BotCommand(command="start",
                   description="Запустить бота"),
        BotCommand(command="admin",
                   description="[Admin] Админ-меню"),
    ]

    await bot.set_my_commands(
        commands=user_commands, scope=BotCommandScopeAllPrivateChats()
    )

    await bot.set_my_commands(
        commands=admin_chat_commands,
        scope=BotCommandScopeAllChatAdministrators()
    )

    await bot.set_my_commands(
        commands=chat_commands, scope=BotCommandScopeAllGroupChats()
    )

    admins = config.misc.admins + config.misc.owners

    for admin_id in admins:
        try:
            await bot.set_my_commands(
                commands=admins_commands,
                scope=BotCommandScopeChat(chat_id=admin_id)
            )
        except TelegramBadRequest:
            logger.error(f"Set My Commands Admin(id={admin_id}): Chat not found")
