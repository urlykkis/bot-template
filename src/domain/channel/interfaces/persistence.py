from asyncio import Protocol

from src.infrastructure.database.models import Channel


class IChannelRepo(Protocol):
    def __init__(self):
        self.session = ...

    """Интерфейс для репозитория с канала"""
    async def add_channel(self, chat: Channel):
        ...

    async def get_by_id(self, chat_id: int) -> Channel:
        ...

    async def edit_channel(self, channel: Channel) -> Channel:
        ...

    async def delete_channel(self, channel: Channel) -> bool:
        ...
