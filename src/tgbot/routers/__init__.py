from aiogram import Router

from . import user, chat, channel, admin, error, unrecognized, owner

router = Router(name="main_router")

router.include_router(user.router)
router.include_router(channel.router)
router.include_router(chat.router)
router.include_router(admin.router)
router.include_router(owner.router)

router.include_router(unrecognized.router)
# router.include_router(error.router)


__all__ = ['router']
