import pytest

from contextlib import nullcontext as does_not_raise, suppress

from src.domain.chat.usecase.chat import ChatService
from src.domain.chat.dto.chat import ChatCreateDTO, PatchChatData, \
    ChatMigratedDTO
from src.domain.chat.exceptions.chat import ChatAlreadyExists, ChatMigrateException

from tests.utils.asserts.chat import assert_chat
from tests.parametrize.chat import \
    get_parametrize_for_get_chat, \
    get_parametrize_for_register_chat, \
    get_parametrize_for_get_registered_chat, \
    get_parametrize_for_patch_chat, \
    get_parametrize_for_delete_chat


class TestChatRepository:
    """Тестирует методы репозитория чата"""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("chat_id", "expected"),
        get_parametrize_for_get_chat()
    )
    async def test_repository_get_chat(
            self, chat_service: ChatService,
            chat_id, expected
    ):
        """Тестирует, что незарегистрированный пользователь правильно возвращается"""
        with expected:
            chat = await chat_service.get_chat(
                chat_id=chat_id
            )
            assert chat is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("chat_data", "expected"),
        get_parametrize_for_register_chat()
    )
    async def test_repository_register_chat(
            self, chat_service: ChatService,
            chat_data: dict, expected
    ):
        """Тестирует, что данные для регистрации пользователя верны и возвращается в DTO"""
        await chat_service.uow.chat.session.rollback()

        with expected:
            chat = await chat_service.register_chat(
                chat=ChatCreateDTO(**chat_data)
            )

            assert_chat(chat)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("chat_data", "expected"),
        get_parametrize_for_get_registered_chat()
    )
    async def test_repository_get_chat_registered(
            self, chat_service: ChatService,
            chat_data, expected
    ):
        """Тестирует, что зарегистрированный юзер возвращается в DTO"""
        await chat_service.uow.chat.session.rollback()

        with expected:
            chat_created = await chat_service.register_chat(
                chat=ChatCreateDTO(**chat_data)
            )

            chat = await chat_service.get_chat(
                chat_id=chat_created.chat_id
            )
            assert_chat(chat)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("chat_data", "patch_data", "expected"),
        get_parametrize_for_patch_chat()
    )
    async def test_repository_patch_chat(
            self, chat_service: ChatService,
            chat_data, patch_data, expected
    ):
        """Тестирует изменения юзера в БД"""
        await chat_service.uow.chat.session.rollback()

        with expected:
            with suppress(ChatAlreadyExists):
                await chat_service.register_chat(
                    chat=ChatCreateDTO(**chat_data)
                )

            chat_patched = await chat_service.patch_chat(
                new_chat=PatchChatData(**patch_data)
            )

            assert_chat(chat_patched)


    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("migrate_data", "expected"),
        [
            ({"old_chat_id": 123, "new_chat_id": 456}, does_not_raise()),
            # ({"old_chat_id": 456, "new_chat_id": 456}, pytest.raises(ChatMigrateException)),
        ]
    )
    async def test_migrate_chat_id(
            self, chat_service: ChatService,
            migrate_data, expected
    ):
        with suppress(ChatAlreadyExists):
            chat_data = ChatCreateDTO(
                chat_id=migrate_data["old_chat_id"],
                title="1",
                is_super_group=True,
                is_forum=True,
                user_id=0,
                members_count=0,
                username="1",
            )
            await chat_service.register_chat(chat=chat_data)

        with expected:
            migrated_chat = await chat_service.migrate_chat(
                migrate_chat=ChatMigratedDTO(**migrate_data)
            )

            assert_chat(migrated_chat)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("chat_data", "delete_id", "expected"),
        get_parametrize_for_delete_chat()
    )
    async def test_repository_delete_chat(
            self, chat_service: ChatService,
            chat_data, delete_id, expected
    ):
        """Тестирует изменения канала в БД"""
        await chat_service.uow.chat.session.rollback()

        with expected:
            with suppress(ChatAlreadyExists):
                await chat_service.register_chat(
                    chat=ChatCreateDTO(**chat_data)
                )

            chat_deleted = await chat_service.delete_chat(
                chat_id=delete_id
            )

            assert chat_deleted is True
