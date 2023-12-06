from sqlalchemy import (select)
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import CheckViolationError

from src.infrastructure.database.repositories.database \
    import SQLAlchemyRepository
from src.domain.channel.interfaces.persistence import IChannelRepo
from src.infrastructure.database.models import Channel
from src.domain.channel.exceptions import \
    ChannelDeleteException, ChannelEditException, ChannelNotExists, \
    ChannelAlreadyExists


class ChannelRepository(SQLAlchemyRepository, IChannelRepo):
    """Репозиторий для работы с каналом"""
    async def add_channel(self, channel: Channel) -> Channel:
        """Создает канал"""
        try:
            self.session.add(channel)
            await self.session.flush()
        except IntegrityError as err:
            if 'asyncpg.exceptions.CheckViolationError' in err.orig.args[0]:
                raise CheckViolationError("channel table")
            raise ChannelAlreadyExists from err

        return channel

    async def get_by_id(self, chat_id: int) -> Channel:
        """Выдает канал по chat_id"""
        stmt = select(Channel).where(Channel.chat_id == chat_id)
        result = await self.session.scalar(stmt)

        if not result:
            raise ChannelNotExists(chat_id)

        return result

    async def edit_channel(self, channel: Channel) -> Channel:
        """Редактирует канал"""
        try:
            self.session.add(channel)
            await self.session.flush()
        except IntegrityError as err:
            raise ChannelEditException(err)

        return channel

    async def delete_channel(self, channel: Channel) -> bool:
        """Удаляет канал"""
        try:
            await self.session.delete(channel)
            await self.session.flush()
            return True
        except IntegrityError as err:
            raise ChannelDeleteException(err)

    async def get_broadcast_recipients_ids(self) -> list[int]:
        stmt = select(Channel.chat_id)
        return list(await self.session.scalars(stmt))

    async def count(self) -> int:
        return await self.count_model(Channel)
