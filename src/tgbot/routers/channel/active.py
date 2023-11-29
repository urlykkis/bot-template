from aiogram import Router
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.types import ChatMemberUpdated

from src.domain.channel.usecase import ChannelService
from src.domain.channel.dto import ChannelCreateDTO

router = Router(name="channel_active")


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION),
)
async def block_channel_handler(
        event: ChatMemberUpdated,
        channel_service: ChannelService
):
    """Бот удален в канале"""
    return await channel_service.delete_channel(chat_id=event.chat.id)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
)
async def new_channel_handler(
        event: ChatMemberUpdated,
        channel_service: ChannelService
):
    """Бот добавлен в канал"""
    # members_count = event.chat.get_member_count() wait for update this method
    # print(members_count)

    return await channel_service.register_channel(
        channel=ChannelCreateDTO(
            chat_id=event.chat.id,
            title=event.chat.title,
            user_id=event.from_user.id,
            members_count=0,
            username=event.chat.username,
        )
    )
