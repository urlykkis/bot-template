from abc import ABC
from typing import Optional
from asyncpg.exceptions import CheckViolationError
from sqlalchemy import (text)

from src.domain.channel.interfaces.uow import IChannelUoW
from src.domain.channel.dto import ChannelDTO, \
    ChannelCreateDTO, PatchChannelData
from src.infrastructure.database.models import Channel
from src.domain.channel.exceptions import \
    ChannelDeleteException, ChannelEditException, \
    ChannelNotExists, ChannelAlreadyExists
from src.infrastructure.logging import logger


class ChannelUseCase(ABC):
    """Основа для UseCase канала"""
    def __init__(self, uow: IChannelUoW) -> None:
        self.uow = uow


class GetChannel(ChannelUseCase):
    """Возвращает сущность канала по chat_id"""
    async def __call__(self, chat_id: int) -> ChannelDTO:
        return ChannelDTO.model_validate(
            await self.uow.channel.get_by_id(chat_id=chat_id)
        )


class RegisterChannel(ChannelUseCase):
    """Создает канал в БД и возвращает его сущность"""
    async def __call__(self, channel: ChannelCreateDTO) -> ChannelDTO:
        _channel = Channel(**channel.model_dump())

        try:
            await self.uow.channel.add_channel(_channel)
            await self.uow.commit()

            logger.info(f"Channel(id={_channel.chat_id}) created")
        except CheckViolationError as err:
            logger.error(f"ChannelAlreadyExists: {err}")
            await self.uow.rollback()
            raise CheckViolationError from err

        except ChannelAlreadyExists as err:
            logger.error(f"ChannelAlreadyExists: {err}")
            await self.uow.rollback()
            raise ChannelAlreadyExists from err

        return ChannelDTO.model_validate(_channel)


class PatchChannel(ChannelUseCase):
    """Редактирует канал и возвращает его новую сущность"""
    async def __call__(self, new_channel: PatchChannelData) -> Optional[ChannelDTO]:
        channel = await self.uow.channel.get_by_id(chat_id=new_channel.chat_id)

        if new_channel.title is not None:
            channel.title = new_channel.title
        if new_channel.members_count is not None:
            channel.members_count = new_channel.members_count

        try:
            channel = await self.uow.channel.edit_channel(channel)
            await self.uow.commit()
        except ChannelEditException as err:
            logger.error(f"ChannelEditException: {err}")
            await self.uow.rollback()
            raise ChannelEditException from err

        channel_dto = ChannelDTO.model_validate(channel)
        logger.info(f"Patch Channel: Data({channel_dto})")
        return channel_dto


class DeleteChannel(ChannelUseCase):
    """Удаляет чат по его chat_id в БД"""
    async def __call__(self, chat_id: int) -> bool:
        try:
            channel = await self.uow.channel.get_by_id(chat_id=chat_id)
        except ChannelNotExists as err:
            logger.error(f"ChannelNotExists (DeleteChannel): {err}")
            await self.uow.rollback()
            raise ChannelNotExists from err

        try:
            await self.uow.channel.delete_channel(channel=channel)
            await self.uow.commit()
            return True
        except ChannelDeleteException as err:
            logger.error(f"ChannelDeleteException: {err}")
            await self.uow.rollback()
            raise ChannelDeleteException from err


class ChannelService:
    """Сервис для упрощения работы с UseCase канала"""
    def __init__(self, uow: IChannelUoW) -> None:
        self.uow = uow

    async def get_channel(self, chat_id: int) -> ChannelDTO:
        return await GetChannel(uow=self.uow)(chat_id=chat_id)

    async def register_channel(self, channel: ChannelCreateDTO) -> ChannelDTO:
        return await RegisterChannel(uow=self.uow)(channel=channel)

    async def patch_channel(
            self,
            new_channel: PatchChannelData
    ) -> ChannelDTO:
        return await PatchChannel(uow=self.uow)(new_channel=new_channel)

    async def delete_channel(self, chat_id: int) -> bool:
        return await DeleteChannel(uow=self.uow)(chat_id=chat_id)
