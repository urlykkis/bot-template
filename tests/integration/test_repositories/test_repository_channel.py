import pytest

from contextlib import nullcontext as does_not_raise, suppress
from pydantic import ValidationError
from sqlalchemy.exc import ProgrammingError, DBAPIError

from src.domain.channel.usecase.channel import ChannelService
from src.domain.channel.dto.channel import ChannelCreateDTO, PatchChannelData
from src.domain.channel.exceptions.channel import ChannelNotExists, \
    ChannelAlreadyExists, ChannelDeleteException

from tests.utils.asserts.channel import assert_channel
from tests.parametrize.channel import \
    get_parametrize_for_get_channel, \
    get_parametrize_for_register_channel, \
    get_parametrize_for_patch_chat


class TestChannelRepository:
    """Тестирует методы репозитория чата"""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("chat_id", "expected"),
        get_parametrize_for_get_channel()
    )
    async def test_repository_get_channel(
            self, channel_service: ChannelService,
            chat_id, expected
    ):
        """Тестирует, что незарегистрированный канал правильно возвращается"""
        with expected:
            chat = await channel_service.get_channel(
                chat_id=chat_id
            )
            assert chat is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("channel_data", "expected"),
        get_parametrize_for_register_channel()
    )
    async def test_repository_register_chat(
            self, channel_service: ChannelService,
            channel_data: dict, expected
    ):
        """Тестирует, что данные для регистрации канала верны и возвращается в DTO"""
        await channel_service.uow.channel.session.rollback()

        with expected:
            chat = await channel_service.register_channel(
                channel=ChannelCreateDTO(**channel_data)
            )

            assert_channel(chat)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("channel_data", "expected"),
        [
            ({"chat_id": 505, "title": "1", "user_id": 1, "members_count": 0, "username": "6345"}, does_not_raise()),
            ({"chat_id": 505, "title": "1", "user_id": 1, "members_count": 0, "username": "6345"}, pytest.raises(ChannelAlreadyExists)),
            ({"chat_id": None, "title": "1", "user_id": 1, "members_count": 0,  "username": "6345"}, pytest.raises(ValidationError)),
            ({"chat_id": 12345678901234567890123456789, "title": "2", "user_id": 1, "members_count": 0, "username": "6345"}, pytest.raises(DBAPIError)),
        ]
    )
    async def test_repository_get_channel_registered(
            self, channel_service: ChannelService,
            channel_data, expected
    ):
        """Тестирует, что зарегистрированный канал возвращается в DTO"""
        await channel_service.uow.channel.session.rollback()

        with expected:
            chat_created = await channel_service.register_channel(
                channel=ChannelCreateDTO(**channel_data)
            )

            chat = await channel_service.get_channel(
                chat_id=chat_created.chat_id
            )
            assert_channel(chat)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("channel_data", "patch_data", "expected"),
        get_parametrize_for_patch_chat()
    )
    async def test_repository_patch_channel(
            self, channel_service: ChannelService,
            channel_data, patch_data, expected
    ):
        """Тестирует изменения канала в БД"""
        await channel_service.uow.channel.session.rollback()

        with expected:
            with suppress(ChannelAlreadyExists):
                await channel_service.register_channel(
                    channel=ChannelCreateDTO(**channel_data)
                )

            chat_patched = await channel_service.patch_channel(
                new_channel=PatchChannelData(**patch_data)
            )

            assert_channel(chat_patched)
    #
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("channel_data", "delete_id", "expected"),
        [
            (
                    {"chat_id": 505, "title": "2", "user_id": 1, "members_count": 0, "username": "6345"},
                    505, does_not_raise()
            ),
            (
                    {"chat_id": 505, "title": "2", "user_id": 1,
                     "members_count": 0, "username": "6345"},
                    None, pytest.raises(ChannelNotExists)
            ),
        ]
    )
    async def test_repository_delete_channel(
            self, channel_service: ChannelService,
            channel_data, delete_id, expected
    ):
        """Тестирует изменения канала в БД"""
        await channel_service.uow.channel.session.rollback()

        with expected:
            with suppress(ChannelAlreadyExists):
                await channel_service.register_channel(
                    channel=ChannelCreateDTO(**channel_data)
                )

            chat_deleted = await channel_service.delete_channel(
                chat_id=delete_id
            )

            assert chat_deleted is True
