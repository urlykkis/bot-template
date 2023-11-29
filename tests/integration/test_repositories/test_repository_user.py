import pytest

from contextlib import nullcontext as does_not_raise, suppress
from pydantic import ValidationError
from sqlalchemy.exc import ProgrammingError, DBAPIError

from src.domain.user.usecase.user import UserService
from src.domain.user.dto.user import UserCreateDTO, PatchUserData
from src.domain.user.exceptions.user import UserNotExists, UserAlreadyExists

from tests.utils.asserts.user import assert_user
from tests.parametrize.user import \
    get_parametrize_for_get_user, \
    get_parametrize_for_register_user,\
    get_parametrize_for_patch_user


class TestUserRepository:
    """Тестирует методы репозитория пользователя"""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("user_id", "expected"),
        get_parametrize_for_get_user()
    )
    async def test_repository_get_user(
            self, user_service: UserService,
            user_id, expected
    ):
        """Тестирует, что незарегистрированный пользователь правильно возвращается"""
        with expected:
            usr = await user_service.get_user(
                user_id=user_id
            )
            assert usr is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("user_data", "expected"),
        get_parametrize_for_register_user(),
    )
    async def test_repository_register_user(
            self, user_service: UserService,
            user_data: dict, expected
    ):
        """Тестирует, что данные для регистрации пользователя верны и возвращается в DTO"""
        # user_service.uow.user.session: AsyncSession
        await user_service.uow.user.session.rollback()

        with expected:
            user = await user_service.register_user(
                user=UserCreateDTO(**user_data)
            )

            assert_user(user)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("user_data", "expected"),
        [
            ({"user_id": 505, "first_name": "1"}, does_not_raise()),
            ({"user_id": 505, "first_name": "1"}, pytest.raises(UserAlreadyExists)),
            ({"user_id": None, "first_name": "1"}, pytest.raises(ValidationError)),
            ({"user_id": 12345678901234567890123456789, "first_name": "2"}, pytest.raises(DBAPIError)),
        ]
    )
    async def test_repository_get_user_registered(
            self, user_service: UserService,
            user_data, expected
    ):
        """Тестирует, что зарегистрированный юзер возвращается в DTO"""
        await user_service.uow.user.session.rollback()

        with expected:
            user_created = await user_service.register_user(
                user=UserCreateDTO(**user_data)
            )

            user = await user_service.get_user(
                user_id=user_created.user_id
            )
            assert_user(user)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("user_data", "patch_data", "expected"),
        get_parametrize_for_patch_user()
    )
    async def test_repository_patch_user(
            self, user_service: UserService,
            user_data, patch_data, expected
    ):
        """Тестирует изменения юзера в БД"""
        await user_service.uow.user.session.rollback()

        with expected:
            with suppress(UserAlreadyExists):
                await user_service.register_user(
                    user=UserCreateDTO(**user_data)
                )

            user_patched = await user_service.patch_user(
                new_user=PatchUserData(**patch_data)
            )

            assert_user(user_patched)
