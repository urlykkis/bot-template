from aiogram import Router, F

from . import active


router = Router(name="channel_main_router")

router.include_router(active.router)

router.my_chat_member.filter(F.chat.type.in_({"channel"}))
router.message.filter(F.chat.type.in_({"channel"}))
router.callback_query.filter(F.chat.type.in_({"channel"}))

__all__ = ['router']
