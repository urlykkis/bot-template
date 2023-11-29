from src.domain.user.interfaces.persistence import IUserRepo
from src.domain.base.interfaces.uow import IUoW


class IUserUoW(IUoW):
    """Интерфейс Unit of Work для работы с пользователем"""
    user: IUserRepo
