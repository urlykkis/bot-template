from aiogram import Router, F
from aiogram.enums import ChatType

from . import start, active, default_commands, default_callbacks


router = Router(name="user_main_router")

router.include_router(start.router)
router.include_router(active.router)
router.include_router(default_commands.router)
router.include_router(default_callbacks.router)

router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)

__all__ = ['router']
