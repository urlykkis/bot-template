from typing import Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.exceptions import CommitError, RollbackError
from src.domain.user.interfaces.persistence import IUserRepo
from src.domain.chat.interfaces.persistence import IChatRepo
from src.domain.channel.interfaces.persistence import IChannelRepo

from src.domain.user.interfaces.uow import IUserUoW
from src.infrastructure.database.uow.alchemy.interface import SQLAlchemyIUoW
from src.infrastructure.logging import logger


class SQLAlchemyUoW(SQLAlchemyIUoW, IUserUoW):
    """Unit of Work для работы с SQLAlchemy"""
    user: IUserRepo
    chat: IChatRepo
    channel: IChatRepo

    def __init__(
            self,
            session: AsyncSession,
            user_repo: Type[IUserRepo],
            chat_repo: Type[IChatRepo],
            channel_repo: Type[IChannelRepo],
    ):
        self.user = user_repo(session)
        self.chat = chat_repo(session)
        self.channel = channel_repo(session)
        super().__init__(session)

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            logger.error(err)
            raise CommitError(err)

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError(err)
