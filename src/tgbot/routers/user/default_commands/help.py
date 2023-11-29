from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from fluentogram import TranslatorRunner

router = Router(name="user_help")


@router.message(Command('help'))
async def help_handler(
        message: Message,
        i18n: TranslatorRunner
):
    """Команда помощи /help"""
    return await message.answer(i18n.user.help())
