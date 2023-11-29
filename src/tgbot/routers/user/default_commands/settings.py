from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from fluentogram import TranslatorRunner

router = Router(name="user_settings")


@router.message(Command('settings'))
async def settings_handler(
        message: Message,
        i18n: TranslatorRunner
):
    """Команда настройки /settings"""
    return await message.answer(i18n.user.settings())
