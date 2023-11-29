from typing import Any

from types import NoneType

from src.domain.chat.dto.chat import ChatDTO


def assert_chat(chat: Any) -> None:
    """Проверяет чат"""
    assert isinstance(chat, ChatDTO)
    assert chat.chat_id is not None and isinstance(chat.chat_id, int)
    assert chat.user_id is not None and isinstance(chat.user_id, int)
    assert chat.members_count is not None and isinstance(chat.members_count, int)
    assert type(chat.username) in [str, NoneType]
    assert isinstance(chat.is_super_group, bool)
    assert isinstance(chat.is_forum, bool)
    assert len(chat.title) <= 256

    if chat.username is not None:
        assert len(chat.username) <= 256
