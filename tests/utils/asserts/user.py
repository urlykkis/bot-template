from typing import Any

from types import NoneType

from src.domain.user.dto.user import UserDTO


def assert_user(user: Any) -> None:
    """Проверяет юзера"""
    assert isinstance(user, UserDTO)
    assert user.user_id is not None and isinstance(user.user_id, int)
    assert type(user.username) in [str, NoneType]
    assert isinstance(user.first_name, str)
    assert type(user.last_name) in [str, NoneType]
    assert isinstance(user.language_code, str)
    assert isinstance(user.active, bool)
    assert len(user.first_name) <= 256

    if user.last_name is not None:
        assert len(user.last_name) <= 256
    if user.username is not None:
        assert len(user.username) <= 256

    assert user.href == f"<a href='tg://user?id={user.user_id}'>{user.full_name}</a>"
    assert repr(user) == f"User(id={user.user_id}, username={user.username}, active={user.active})"
