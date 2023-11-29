from asyncio import Protocol

from src.infrastructure.database.models import User


class IUserRepo(Protocol):
    """Интерфейс для репозитория с пользователем"""
    def __init__(self):
        self.session = ...

    async def add_user(self, user: User):
        ...

    async def get_by_id(self, user_id: int) -> User:
        ...

    async def edit_user(self, user: User) -> User:
        ...
