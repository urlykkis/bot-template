from src.domain.base.exceptions import AppException

from src.infrastructure.database.models.user import User


class UserException(AppException):
    """Ошибка при работе с пользователем"""


class UserNotExists(UserException):
    """Пользователь не существует в БД"""


class UserAlreadyExists(UserException):
    """Пользователь уже существует в БД"""
    user: User


class UserEditException(UserException):
    """Ошибка при редактировании пользователя в БД"""


class UserDeleteException(UserException):
    """Ошибка при удалении пользователя в БД"""
