from sqlalchemy import (String, Boolean, BigInteger)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.mixin \
    import ModelWithTime, UserIDMixin, UsernameMixin


class User(Base, UserIDMixin, ModelWithTime, UsernameMixin):
    """Модель пользователя"""
    __tablename__ = "user"

    _primary_key = True
    _index = True

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_premium: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(256),
        nullable=True,
    )
    language_code: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="en",
    )
