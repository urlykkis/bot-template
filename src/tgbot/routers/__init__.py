from aiogram import Router, Dispatcher

from . import user, chat, channel, admin, error, unrecognized, owner

main_router = Router(name="main_router")

main_router.include_router(user.router)
main_router.include_router(channel.router)
main_router.include_router(chat.router)
main_router.include_router(admin.router)
main_router.include_router(owner.router)

main_router.include_router(unrecognized.router)
# router.include_router(error.router)


def register_routers(dp: Dispatcher):
    dp.include_router(main_router)
