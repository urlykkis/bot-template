from aiogram import Router, F
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated

from src.domain.user.usecase import UserService
from src.domain.user.dto import PatchUserData

router = Router()


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER)
)
async def user_blocked_bot(
        event: ChatMemberUpdated,
        user_service: UserService
):
    """Пользователь заблокировал бота"""
    return await user_service.patch_user(
        new_user=PatchUserData(user_id=event.from_user.id, active=False)
    )


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER)
)
async def user_unblocked_bot(
        event: ChatMemberUpdated,
        user_service: UserService
):
    """Пользователь разблокировал бота"""
    return await user_service.patch_user(
        new_user=PatchUserData(user_id=event.from_user.id, active=True)
    )
