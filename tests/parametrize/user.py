import pytest

from contextlib import nullcontext as does_not_raise
from pydantic import ValidationError
from sqlalchemy.exc import ProgrammingError, DBAPIError

from src.domain.user.exceptions.user import UserNotExists, UserAlreadyExists


def get_parametrize_for_get_user():
    return [
            (1, pytest.raises(UserNotExists)),
            (12345678901234, pytest.raises(UserNotExists)),
            (-1, pytest.raises(UserNotExists)),
            (12345678901234567890123456789, pytest.raises(DBAPIError)),
            ("1", pytest.raises(ProgrammingError)),
            (None, pytest.raises(DBAPIError)),
            (True, pytest.raises(DBAPIError)),
            ({"user_id": 1}, pytest.raises(DBAPIError)),
        ]


def get_parametrize_for_register_user():

    return  [
            ({"user_id": 1, "first_name": "1"}, does_not_raise()),
            ({"user_id": 4, "first_name": "2", "last_name": None, "username": None}, does_not_raise()),
            ({"user_id": 2, "first_name": "3", "last_name": "1", "username": "qwe", "language_code": "ru", "is_premium": True}, does_not_raise()),
            ({"user_id": 12345678901234, "first_name": "2"}, does_not_raise()),

            ({"user_id": 1, "first_name": "1"}, pytest.raises(UserAlreadyExists)),
            ({"user_id": "1", "first_name": "2"}, pytest.raises(UserAlreadyExists)),  # is_digit -> True

            ({"user_id": None, "first_name": "1"}, pytest.raises(ValidationError)),
            ({"user_id": 3, "first_name": None}, pytest.raises(ValidationError)),
            ({"user_id": 5, "first_name": "2", "language_code": None, "is_premium": None}, pytest.raises(ValidationError)),
            ({"user_id": 5, "first_name": 3}, pytest.raises(ValidationError)),
            ({"user_id": "1s", "first_name": "2"}, pytest.raises(ValidationError)),
            ({"user_id": -1, "first_name": "2"}, pytest.raises(ValidationError)),

            ({"user_id": 12345678901234567890123456789, "first_name": "2"}, pytest.raises(DBAPIError)),
        ]


def get_parametrize_for_patch_user():
    return [
            ({"user_id": 505, "first_name": "2"}, {"user_id": 505, "first_name": "1"}, does_not_raise()),
            ({"user_id": 505, "first_name": "2"}, {"user_id": 505, "first_name": "4"}, does_not_raise()),

            ({"user_id": 505, "first_name": "2"},
             {"user_id": 505, "first_name": "4", "username": "1234567891234567891234567891234545679"}, pytest.raises(ValidationError)),

            ({"user_id": 505, "first_name": "2"}, {"user_id": 505, "first_name": "4", "active": "v534"},  pytest.raises(ValidationError)),
            ({"user_id": 505, "first_name": "2"}, {"user_id": 505, "first_name": "4", "is_premium": "v534"}, pytest.raises(ValidationError)),
        ]
