from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.mixin import ChatMixin


class Channel(Base, ChatMixin):
    """Модель канала"""
    __tablename__ = "channel"
