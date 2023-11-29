from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class ModelWithID:
    """Основа для моделей, который возвращает колонку id_"""

    id_: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
    )
