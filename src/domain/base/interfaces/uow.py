from asyncio import Protocol


class IUoW(Protocol):
    """Интерфейс Unit of Work"""

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...
