from src.domain.base.exceptions import AppException


class ChatException(AppException):
    """Ошибка при работе с чатом"""


class ChatNotExists(ChatException):
    """Чат не существует в БД"""


class ChatAlreadyExists(ChatException):
    """Чат уже существует в БД"""


class ChatEditException(ChatException):
    """Ошибка при редактировании чата"""


class ChatDeleteException(ChatException):
    """Ошибка при удалении чата"""


class ChatMigrateException(ChatException):
    """Ошибка при удалении чата"""
