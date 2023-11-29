from asyncio import Protocol

from src.infrastructure.database.models import Chat


class IChatRepo(Protocol):
    """Интерфейс для репозитория с чатом"""
    def __init__(self):
        self.session = ...

    async def add_chat(self, chat: Chat):
        ...

    async def get_by_id(self, chat_id: int) -> Chat:
        ...

    async def edit_chat(self, chat: Chat) -> Chat:
        ...

    async def delete_chat(self, chat: Chat) -> bool:
        ...
