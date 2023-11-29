from typing import Optional

from pydantic import Field

from src.domain.base.dto.base import DTO


class UserDTO(DTO):
    """Сущность пользователя"""
    user_id: int = Field(..., ge=0)
    username: Optional[str]
    active: bool
    is_premium: bool
    first_name: str
    last_name: Optional[str]
    language_code: str

    def __repr__(self):
        return f"User(id={self.user_id}, username={self.username}, active={self.active})"

    @property
    def full_name(self):
        """Возвращает полное имя"""
        last_name = self.last_name if self.last_name is not None else ""
        return f"{self.first_name} {last_name}"

    @property
    def href(self):
        return f"<a href='tg://user?id={self.user_id}'>{self.full_name}</a>"

    def __eq__(self, other):
        if not isinstance(other, UserCreateDTO):
            return False
        else:
            other: UserCreateDTO
            my_dump = self.model_dump()
            other_dump = other.model_dump()

            for key, value in other_dump:
                if value != my_dump[key]:
                    return False

        return True


class UserCreateDTO(DTO):
    """Сущность для создания пользователя"""
    user_id: int = Field(..., ge=0)
    username: Optional[str] = Field(None, max_length=32)
    is_premium: bool = False
    first_name: str = Field(..., max_length=256)
    last_name: Optional[str] = Field(None, max_length=256)
    language_code: str = "en"


class PatchUserData(DTO):
    """Сущность для редактирования пользователя"""
    user_id: int = Field(..., ge=0)
    username: Optional[str] = Field(None, max_length=32)
    active: Optional[bool] = None
    first_name: Optional[str] = Field(None, max_length=256)
    last_name: Optional[str] = Field(None, max_length=256)
    is_premium: Optional[bool] = None
    language_code: Optional[str] = Field(None, max_length=32)

    @property
    def updated_data(self) -> dict:
        new_user = self.model_dump()
        new_data = {}

        for key, value in new_user.items():
            if value is not None:
                new_data[key] = value

        return new_data
