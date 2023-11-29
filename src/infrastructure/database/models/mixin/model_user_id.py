from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, declared_attr


class UserIDMixin:
    """Основа для моделей, который возвращает колонку с ID пользователя"""
    _primary_key: bool = True

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            BigInteger,
            primary_key=cls._primary_key,
            index=True,
    )
