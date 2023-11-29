from aiogram import Router

from src.tgbot.common.filters import OwnerFilter

from . import menu

router = Router(name="owner_main_router")

router.message.filter(OwnerFilter())

router.include_router(menu.router)


__all__ = ['router']
