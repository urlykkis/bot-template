from sqlalchemy import (select)
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import CheckViolationError

from src.infrastructure.database.repositories.database \
    import SQLAlchemyRepository
from src.domain.user.interfaces.persistence import IUserRepo
from src.infrastructure.database.models import User
from src.domain.user.exceptions import \
    UserNotExists, UserAlreadyExists, \
    UserEditException, UserDeleteException


class UserRepository(SQLAlchemyRepository, IUserRepo):
    """Репозиторий для работы с пользователем"""
    async def add_user(self, user: User) -> User:
        """Создает пользователя"""
        try:
            self.session.add(user)
            await self.session.flush()
        except IntegrityError as err:
            if 'asyncpg.exceptions.CheckViolationError' in err.orig.args[0]:
                raise CheckViolationError("user table")
            raise UserAlreadyExists from err

        return user

    async def get_by_id(self, user_id: int) -> User:
        """Выдает пользователя по user_id"""
        stmt = select(User).where(User.user_id == user_id)
        result = await self.session.scalar(stmt)

        if not result:
            raise UserNotExists(user_id)

        return result

    async def edit_user(self, user: User) -> User:
        """Редактирует пользователя"""
        try:
            self.session.add(user)
            await self.session.flush()
        except IntegrityError as err:
            raise UserEditException(err)

        return user

    async def delete_user(self, user: User) -> bool:
        """Удаляет чат"""
        try:
            await self.session.delete(user)
            await self.session.flush()
            return True
        except IntegrityError as err:
            raise UserDeleteException(err)

    async def count(self) -> int:
        return await self.count_model(User)

    async def get_broadcast_recipients_ids(self) -> list[int]:
        stmt = select(User.user_id).filter(User.active == True)
        return list(await self.session.scalars(stmt))
