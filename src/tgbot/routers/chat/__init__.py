from aiogram import Router, F

from . import active


router = Router(name="chat_main_router")

router.include_router(active.router)

router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))
router.message.filter(F.chat.type.in_({"group", "supergroup"}))
router.callback_query.filter(F.chat.type.in_({"group", "supergroup"}))

__all__ = ['router']
