import pytest

from contextlib import nullcontext as does_not_raise
from pydantic import ValidationError
from sqlalchemy.exc import ProgrammingError, DBAPIError

from src.domain.channel.exceptions.channel import ChannelNotExists, \
    ChannelAlreadyExists


def get_parametrize_for_get_channel():
    return [
        (1, pytest.raises(ChannelNotExists)),
        (12345678901234, pytest.raises(ChannelNotExists)),
        (-1, pytest.raises(ChannelNotExists)),
        (12345678901234567890123456789, pytest.raises(DBAPIError)),
        ("1", pytest.raises(ProgrammingError)),
        (None, pytest.raises(DBAPIError)),
        (True, pytest.raises(DBAPIError)),
        ({"chat_id": 1}, pytest.raises(DBAPIError)),
    ]


def get_parametrize_for_register_channel():
    return [
        (
            {"chat_id": 1, "title": "1", "user_id": 1, "members_count": 0},
            does_not_raise()
        ),
        (
            {"chat_id": 1, "title": "1", "user_id": 1, "members_count": 0,
             "username": "123"}, pytest.raises(ChannelAlreadyExists)
        ),
        (
            {"chat_id": 2, "title": "1", "user_id": 1, "members_count": 0,
             "username": "123"}, does_not_raise()
        ),
        (
            {"chat_id": 12345678901234567890123456789, "title": "1",
             "user_id": 1, "members_count": 0, "username": "6345"},
            pytest.raises(DBAPIError)
        ),
        (
            {"chat_id": "1s", "title": "1", "user_id": 1, "members_count": 0,
             "username": "143"}, pytest.raises(ValidationError)
        ),
        (
            {"chat_id": "123", "title": "1", "user_id": 1, "members_count": 0,
             "username": "2345234523452345234523452345"}, does_not_raise()
        # is_digit -> True
        ),
    ]


def get_parametrize_for_patch_chat():
    return [
        (
            {"chat_id": 505, "title": "2", "user_id": 1, "members_count": 0,
             "username": "6345"},
            {"chat_id": 505, "title": "1", "user_id": 1, "members_count": 0,
             "username": "6345"},
            does_not_raise()
        ),
        (
            {"chat_id": 505, "title": "2", "user_id": 1, "members_count": 0,
             "username": "6345"},
            {"chat_id": 505, "title": "4",
             "username": "1234567891234567891234567891234545671231239",
             "user_id": 1, "members_count": 0},
            pytest.raises(ValidationError)
        ),
        (
            {"chat_id": 505, "title": "2", "user_id": 1, "members_count": 0,
             "username": "6345"},
            {"chat_id": 505, "title": "4", "members_count": "534",
             "user_id": 1, "username": "6345"},
            does_not_raise()
        ),
        (
            {"chat_id": 505, "title": "2", "user_id": 1, "members_count": 0,
             "username": "6345"},
            {"chat_id": 505, "title": "4", "user_id": "534",
             "members_count": 0, "username": "6345"},
            does_not_raise()
        ),
        (
            {"chat_id": 505, "title": "2", "user_id": 1, "members_count": 0,
             "username": "6345"},
            {"chat_id": 505, "title": "4", "user_id": None, "members_count": 0,
             "username": "6345"},
            does_not_raise()
        ),
    ]
