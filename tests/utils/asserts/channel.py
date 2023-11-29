from typing import Any

from types import NoneType

from src.domain.channel.dto.channel import ChannelDTO


def assert_channel(channel: Any) -> None:
    """Проверяет канал"""
    assert isinstance(channel, ChannelDTO)
    assert channel.chat_id is not None and isinstance(channel.chat_id, int)
    assert channel.user_id is not None and isinstance(channel.user_id, int)
    assert channel.members_count is not None and isinstance(channel.members_count, int)
    assert type(channel.username) in [str, NoneType]
    assert len(channel.title) <= 256

    if channel.username is not None:
        assert len(channel.username) <= 256
