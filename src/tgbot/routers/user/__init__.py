from aiogram import Router

from . import start, active, default_commands, default_callbacks


router = Router(name="user_main_router")

router.include_router(start.router)
router.include_router(active.router)
router.include_router(default_commands.router)
router.include_router(default_callbacks.router)

__all__ = ['router']
