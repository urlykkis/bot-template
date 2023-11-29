from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, declared_attr


class UsernameMixin:
    """Основа для моделей, который возвращает колонку с логином"""
    _index: bool = True
    _value_len: int = 256

    @declared_attr
    def username(cls) -> Mapped[str]:
        return mapped_column(
            String(cls._value_len),
            index=cls._index,
            nullable=True,
        )
