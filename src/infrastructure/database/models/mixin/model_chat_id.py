from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class ModelWithChatID:
    """Основа для моделей, который возвращает колонку с ID чата"""

    chat_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
    )
