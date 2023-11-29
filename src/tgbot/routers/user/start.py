from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluentogram import TranslatorRunner

from src.tgbot.common.keyboards.inline.menu import menu_markup

router = Router(name="start")


@router.message(Command("start"))
async def command_start(message: Message, i18n: TranslatorRunner):
    return await message.answer(
        i18n.user.start(), reply_markup=menu_markup()
    )
