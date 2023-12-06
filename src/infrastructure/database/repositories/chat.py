from sqlalchemy import (select)
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import CheckViolationError

from src.infrastructure.database.repositories.database \
    import SQLAlchemyRepository
from src.domain.chat.interfaces.persistence import IChatRepo
from src.infrastructure.database.models import Chat
from src.domain.chat.exceptions import ChatNotExists, \
    ChatAlreadyExists, ChatEditException, ChatDeleteException


class ChatRepository(SQLAlchemyRepository, IChatRepo):
    """Репозиторий для работы с чатом"""
    async def add_chat(self, chat: Chat) -> Chat:
        """Создает чат"""
        try:
            self.session.add(chat)
            await self.session.flush()
        except IntegrityError as err:
            if 'asyncpg.exceptions.CheckViolationError' in err.orig.args[0]:
                raise CheckViolationError("channel table")
            raise ChatAlreadyExists from err

        return chat

    async def get_by_id(self, chat_id: int) -> Chat:
        """Выдает чат по chat_id"""
        stmt = select(Chat).where(Chat.chat_id == chat_id)
        result = await self.session.scalar(stmt)

        if not result:
            raise ChatNotExists(chat_id)

        return result

    async def edit_chat(self, chat: Chat) -> Chat:
        """Редактирует чат"""
        try:
            self.session.add(chat)
            await self.session.flush()
        except IntegrityError as err:
            raise ChatEditException(err)

        return chat

    async def delete_chat(self, chat: Chat) -> bool:
        """Удаляет чат"""
        try:
            await self.session.delete(chat)
            await self.session.flush()
            return True
        except IntegrityError as err:
            raise ChatDeleteException(err)

    async def get_broadcast_recipients_ids(self) -> list[int]:
        stmt = select(Chat.chat_id)
        return list(await self.session.scalars(stmt))

    async def count(self) -> int:
        return await self.count_model(Chat)
