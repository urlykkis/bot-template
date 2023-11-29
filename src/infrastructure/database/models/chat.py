from sqlalchemy import (Boolean, Integer)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.mixin import ChatMixin


class Chat(Base, ChatMixin):
    """Модель чата"""
    __tablename__ = "chat"

    is_super_group: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    is_forum: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    members_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
