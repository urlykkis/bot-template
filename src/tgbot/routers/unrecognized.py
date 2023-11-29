from aiogram import Router
from aiogram.types import Message
from fluentogram import TranslatorRunner

router = Router()


@router.message()
async def msg_unrecognized(message: Message, i18n: TranslatorRunner):
    """Сообщение, которое не попало в обработчики"""
    return await message.answer(i18n.unrecognized())
