from abc import ABC
from typing import Optional
from asyncpg.exceptions import CheckViolationError

from src.domain.chat.interfaces.uow import IChatUoW
from src.domain.chat.dto import \
    ChatDTO, ChatCreateDTO, \
    PatchChatData, ChatMigratedDTO

from src.infrastructure.database.models import Chat
from src.domain.chat.exceptions import \
    ChatAlreadyExists, ChatEditException, \
    ChatNotExists, ChatDeleteException, ChatMigrateException
from src.infrastructure.logging import logger


class ChatUseCase(ABC):
    """Основа для UseCase чата"""
    def __init__(self, uow: IChatUoW) -> None:
        self.uow = uow


class GetChat(ChatUseCase):
    """Возвращает сущность чата по chat_id"""
    async def __call__(self, chat_id: int) -> ChatDTO:
        return ChatDTO.model_validate(
            await self.uow.chat.get_by_id(chat_id=chat_id)
        )


class RegisterChat(ChatUseCase):
    """Создает чат в БД и возвращает его сущность"""
    async def __call__(self, chat: ChatCreateDTO) -> ChatDTO:
        chat = Chat(**chat.model_dump())

        try:
            await self.uow.chat.add_chat(chat)
            await self.uow.commit()

            logger.info(f"Chat(id={chat.chat_id}) created")
        except CheckViolationError as err:
            logger.error(f"CheckViolationError: {err}")
            await self.uow.rollback()
            raise CheckViolationError from err
        except ChatAlreadyExists as err:
            logger.error(f"ChatAlreadyExists: {err}")
            await self.uow.rollback()
            raise ChatAlreadyExists from err

        return ChatDTO.model_validate(chat)


class PatchChat(ChatUseCase):
    """Редактирует чат и возвращает его новую сущность"""
    async def __call__(self, new_chat: PatchChatData) -> Optional[ChatDTO]:
        chat = await self.uow.chat.get_by_id(chat_id=new_chat.chat_id)

        if new_chat.title is not None:
            chat.title = new_chat.title
        if new_chat.is_forum is not None:
            chat.is_forum = new_chat.is_forum
        if new_chat.is_super_group is not None:
            chat.is_super_group = new_chat.is_super_group
        if new_chat.members_count is not None:
            chat.members_count = new_chat.members_count

        try:
            chat = await self.uow.chat.edit_chat(chat)
            await self.uow.commit()
        except ChatEditException as err:
            logger.error(f"ChatEditException: {err}")
            await self.uow.rollback()
            raise ChatEditException from err

        chat_dto = ChatDTO.model_validate(chat)
        logger.info(f"Patch Chat: Data({chat_dto})")
        return chat_dto


class MigrateChat(ChatUseCase):
    """Редактирует ID чата в БД и возвращает его новую сущность"""
    async def __call__(self, migrate_chat: ChatMigratedDTO) -> ChatDTO:
        chat = await self.uow.chat.get_by_id(chat_id=migrate_chat.old_chat_id)

        chat.chat_id = migrate_chat.new_chat_id

        try:
            chat = await self.uow.chat.edit_chat(chat)
            await self.uow.commit()
        except ChatEditException as err:
            logger.error(f"ChatEditException (ChatMigrate): {err}")
            await self.uow.rollback()
            raise ChatMigrateException from err

        chat_dto = ChatDTO.model_validate(chat)
        logger.info(f"Migrate Chat: {migrate_chat.old_chat_id} -> {migrate_chat.new_chat_id}")
        return chat_dto


class DeleteChat(ChatUseCase):
    """Удаляет чат по его chat_id в БД"""
    async def __call__(self, chat_id: int) -> bool:
        try:
            chat = await self.uow.chat.get_by_id(chat_id)
        except ChatNotExists as err:
            logger.error(f"ChatNotExists (DeleteChat): {err}")
            raise ChatNotExists from err

        try:
            await self.uow.chat.delete_chat(chat=chat)
            await self.uow.commit()
            return True
        except ChatDeleteException as err:
            logger.error(f"ChatDeleteException: {err}")
            await self.uow.rollback()
            raise ChatDeleteException from err


class ChatService:
    """Сервис для упрощения работы с UseCase чата"""
    def __init__(self, uow: IChatUoW) -> None:
        self.uow = uow

    async def get_chat(self, chat_id: int) -> ChatDTO:
        return await GetChat(uow=self.uow)(chat_id=chat_id)

    async def register_chat(self, chat: ChatCreateDTO) -> ChatDTO:
        return await RegisterChat(uow=self.uow)(chat=chat)

    async def patch_chat(
            self,
            new_chat: PatchChatData
    ) -> ChatDTO:
        return await PatchChat(uow=self.uow)(new_chat=new_chat)

    async def delete_chat(self, chat_id: int) -> bool:
        return await DeleteChat(uow=self.uow)(chat_id=chat_id)

    async def migrate_chat(self, migrate_chat: ChatMigratedDTO) -> ChatDTO:
        return await MigrateChat(uow=self.uow)(migrate_chat=migrate_chat)
