from abc import ABC
from typing import Optional
from asyncpg.exceptions import CheckViolationError

from src.domain.user.interfaces.uow import IUserUoW
from src.domain.user.dto import UserDTO, UserCreateDTO, PatchUserData
from src.infrastructure.database.models.user import User
from src.domain.user.exceptions import UserAlreadyExists, UserEditException
from src.infrastructure.logging import logger
from src.infrastructure.database.exceptions import CommitError


class UserUseCase(ABC):
    """Основа для UseCase пользователя"""
    def __init__(self, uow: IUserUoW) -> None:
        self.uow = uow


class GetUser(UserUseCase):
    """Возвращает сущность пользователя по user_id"""
    async def __call__(self, user_id: int) -> UserDTO:
        return UserDTO.model_validate(
            await self.uow.user.get_by_id(user_id=user_id)
        )


class RegisterUser(UserUseCase):
    """Создает пользователя в БД и возвращает его сущность"""
    async def __call__(self, user: UserCreateDTO) -> UserDTO:
        user = User(**user.model_dump())

        try:
            await self.uow.user.add_user(user)
            await self.uow.commit()

            logger.info(f"User(id={user.user_id}) created")
        except CheckViolationError as err:
            logger.error(f"CheckViolationError: {err}")
            await self.uow.rollback()
            raise CheckViolationError from err
        except (UserAlreadyExists, CommitError) as err:
            logger.error(err)
            await self.uow.rollback()
            raise UserAlreadyExists(err) from err

        return UserDTO.model_validate(user)


class PatchUser(UserUseCase):
    """Редактирует пользователя и возвращает его новую сущность"""
    async def __call__(self, new_user: PatchUserData) -> Optional[UserDTO]:
        user = await self.uow.user.get_by_id(user_id=new_user.user_id)

        if new_user.username is not None:
            user.username = new_user.username
        if new_user.active is not None:
            user.active = new_user.active
        if new_user.language_code is not None:
            user.language_code = new_user.language_code
        if new_user.last_name is not None:
            user.last_name = new_user.last_name
        if new_user.first_name is not None:
            user.first_name = new_user.first_name
        if new_user.is_premium is not None:
            user.is_premium = new_user.is_premium

        try:
            user = await self.uow.user.edit_user(user)
            await self.uow.commit()
        except UserEditException as err:
            logger.error(err)
            await self.uow.rollback()

        user_dto = UserDTO.model_validate(user)
        logger.info(f"Patch User: Data({user_dto})")
        return user_dto

    async def check_differences(
            self, event_from_user, user: UserDTO) -> Optional[UserDTO]:
        update_data = {}

        if user.username != event_from_user.username:
            update_data["username"] = event_from_user.username
        if user.language_code != event_from_user.language_code:
            update_data["language_code"] = event_from_user.language_code
        if user.first_name != event_from_user.first_name:
            update_data["first_name"] = event_from_user.first_name
        if user.last_name != event_from_user.last_name:
            update_data["last_name"] = event_from_user.last_name
        if user.is_premium != event_from_user.is_premium:
            update_data["is_premium"] = event_from_user.is_premium

        if bool(update_data):
            update_data["user_id"] = event_from_user.id

            user = await PatchUser(uow=self.uow)(
                new_user=PatchUserData(**update_data)
            )
            return user

        return None


class UserService:
    """Сервис для упрощения работы с UseCase пользователя"""
    def __init__(self, uow: IUserUoW) -> None:
        self.uow = uow

    async def get_user(self, user_id: int) -> UserDTO:
        return await GetUser(uow=self.uow)(user_id=user_id)

    async def register_user(self, user: UserCreateDTO) -> UserDTO:
        return await RegisterUser(uow=self.uow)(user=user)

    async def patch_user(self, new_user: PatchUserData) -> UserDTO:
        return await PatchUser(uow=self.uow)(new_user=new_user)
