from aiogram import Router, F

from . import active


router = Router()

chat_type = {"group", "supergroup"}

chat_type_filter = F.chat.type.in_(chat_type)

router.my_chat_member.filter(chat_type_filter)
router.message.filter(chat_type_filter)
router.callback_query.filter(F.message.chat.in_(chat_type))

router.include_router(active.router)


__all__ = ['router']
