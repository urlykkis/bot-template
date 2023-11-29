from aiogram import Router

from . import default

router = Router(name="error_main_router")

router.include_router(default.router)


__all__ = ['router']
