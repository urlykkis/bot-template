from src.domain.base.exceptions import AppException


class ChannelException(AppException):
    """Ошибка при работе с каналом"""


class ChannelNotExists(ChannelException):
    """Канал не существует в БД"""


class ChannelAlreadyExists(ChannelException):
    """Канал уже существует в БД"""


class ChannelEditException(ChannelException):
    """Ошибка при редактировании канала"""


class ChannelDeleteException(ChannelException):
    """Ошибка при удалении канала"""
