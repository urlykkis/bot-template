from aiogram import Router

from . import help as user_help, settings


router = Router(name="user_default_commands")

router.include_router(user_help.router)
router.include_router(settings.router)

__all__ = ['router']
