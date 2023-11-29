from aiogram import Router, F, Bot
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.types import ChatMemberUpdated, Message

from src.domain.chat.usecase import ChatService
from src.domain.chat.dto import ChatCreateDTO, ChatMigratedDTO

router = Router(name="chat_active")


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION),
)
async def block_chat_handler(
        event: ChatMemberUpdated,
        chat_service: ChatService
):
    """Бот удален в чате"""
    return await chat_service.delete_chat(event.chat.id)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
)
async def new_chat_handler(
        event: ChatMemberUpdated,
        chat_service: ChatService
):
    """Бот добавлен в чат"""
    # members_count = event.chat.get_member_count() wait for update this method
    # print(members_count)

    return await chat_service.register_chat(
        chat=ChatCreateDTO(
            chat_id=event.chat.id,
            title=event.chat.title,
            is_super_group="supergroup" in event.chat.type,
            is_forum=bool(event.chat.is_forum),
            user_id=event.from_user.id,
            members_count=0,
        )
    )


@router.message(F.migrate_to_chat_id)
async def group_to_supergroup_migration(
        message: Message,
        chat_service: ChatService
):
    """Чат мигрировал с обычной группы в супер-группу"""
    return await chat_service.migrate_chat(
        migrate_chat=ChatMigratedDTO(
            old_chat_id=message.chat.id,
            new_chat_id=message.migrate_to_chat_id
        )
    )
