from aiogram import Router, F

from . import active


router = Router(name="channel_main_router")

chat_type = {"channel"}

router.include_router(active.router)

router.my_chat_member.filter(F.chat.type.in_(chat_type))
router.message.filter(F.chat.type.in_(chat_type))
router.callback_query.filter(F.message.chat.type.in_(chat_type))

__all__ = ['router']
