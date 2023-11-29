from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router(name="user_hide")


@router.callback_query(F.data == "hide")
async def hide_handler(call: CallbackQuery):
    """Удаляет (скрывает) сообщение"""
    with suppress(Exception):
        await call.message.delete()

    return True
