from aiogram import Router

from . import cancel, hide


router = Router(name="user_default_callbacks")

router.include_router(hide.router)
router.include_router(cancel.router)

__all__ = ['router']
