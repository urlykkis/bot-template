from src.domain.chat.interfaces.persistence import IChatRepo
from src.domain.base.interfaces.uow import IUoW


class IChatUoW(IUoW):
    """Интерфейс Unit of Work для работы с чатом"""
    chat: IChatRepo
