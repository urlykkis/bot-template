from typing import Union

from random import randint
from datetime import datetime

from aiogram import Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.types import \
    CallbackQuery, Chat, Message, \
    Update, User, ChatMemberUpdated, \
    ChatMemberLeft, ChatMemberMember


def get_update(
        message: Message = None,
        callback_query: CallbackQuery = None,
        my_chat_member: ChatMemberUpdated = None,
        **kwargs
) -> Update:
    """Возвращает объект обновления"""
    upd = Update(
        update_id=randint(0, 9999999),
        message=message,
        callback_query=callback_query or None,
        my_chat_member=my_chat_member or None,
        **kwargs
    )
    return upd


def get_chat_member_updated(
        chat: Chat, user: User,
        old_chat_member = None, new_chat_member = None
) -> Union[ChatMemberUpdated, None]:
    """Возвращает объект обновления пользователя чата"""
    old_chat_member = ChatMemberLeft(user=user) if old_chat_member is None else old_chat_member
    new_chat_member = ChatMemberMember(user=user) if new_chat_member is None else new_chat_member

    if old_chat_member.user.id == user.id and new_chat_member.user.id == user.id:
        return ChatMemberUpdated(
            chat=chat,
            from_user=user,
            date=datetime.now(),
            old_chat_member=old_chat_member,
            new_chat_member=new_chat_member,
        )
    else:
        return None


def get_message(bot: Bot, text: str | None, chat: Chat, from_user: User, **kwargs) -> Message:
    """Возвращает объект сообщения"""
    msg = Message(
        message_id=randint(0, 9999999),
        date=datetime.now(),
        chat=chat,
        from_user=from_user,
        sender_chat=chat,
        text=text,
        **kwargs
    )
    msg._bot = bot
    return msg


def get_callback_query(
    bot: Bot, data: str | CallbackData, user: User, message=None, **kwargs
) -> CallbackQuery:
    """Возвращает объект нажатия кнопки"""
    call = CallbackQuery(
        id='test',
        from_user=user,
        chat_instance='test',
        message=message,
        data=data,
        **kwargs
    )
    call._bot = bot
    return call
