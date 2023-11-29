from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluentogram import TranslatorRunner


router = Router(name="admin_menu")


@router.message(Command("admin"))
async def admin_menu_handler(
        message: Message,
        i18n: TranslatorRunner
):
    """Админ меню /admin"""
    return await message.answer(i18n.admin.menu())
