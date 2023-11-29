from sqlalchemy import (String)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.mixin \
    import ModelWithTime, ModelWithChatID, \
    UserIDMixin, ModelWithMembersCount, UsernameMixin


class ChatMixin(
    UserIDMixin, ModelWithChatID,
    ModelWithTime, ModelWithMembersCount,
    UsernameMixin
):
    """Основа для моделей, который возвращает колонки для работы с чатами
    (Чат/Канал)
    """
    _primary_key = False
    _index = False

    title: Mapped[str] = mapped_column(
        String(256),
        nullable=True,
    )
