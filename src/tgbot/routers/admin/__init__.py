from aiogram import Router

from src.tgbot.common.filters import AdminFilter

from . import menu

router = Router(name="admin_main_router")

router.message.filter(AdminFilter())

router.include_router(menu.router)


__all__ = ['router']
