from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class ModelWithMembersCount:
    """Основа для моделей, который возвращает колонки с кол-вом пользователей"""

    members_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
