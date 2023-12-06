from typing import Optional

from pydantic import Field

from src.domain.base.dto import DTO, PatchDTO


class UserCreateDTO(DTO):
    """Сущность для создания пользователя"""
    user_id: int = Field(..., ge=0)
    username: Optional[str] = Field(None, max_length=32)
    is_premium: bool = False
    first_name: str = Field(..., max_length=256)
    last_name: Optional[str] = Field(None, max_length=256)
    language_code: str = "en"


class UserDTO(UserCreateDTO):
    """Сущность пользователя"""
    active: bool

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

    @property
    def referral_href(self):
        return f"<a href='tg://user?id={self.referred}'>Приглашен этим человеком</a>"

    @property
    def i18n_user(self):
        user_dump = self.model_dump()

        user_dump["last_name"] = user_dump["last_name"] if user_dump["last_name"] is not None else ""
        user_dump["ban"] = "Забанен" if user_dump["ban"] is True else "Не забанен"
        user_dump["is_premium"] = "Да" if user_dump["is_premium"] is True else "Нет"
        user_dump["referred"] = self.referral_href if user_dump["referred"] else "Нет"
        return user_dump


class PatchUserData(PatchDTO):
    """Сущность для редактирования пользователя"""
    user_id: int = Field(..., ge=0)
    username: Optional[str] = Field(None, max_length=32)
    active: Optional[bool] = None
    first_name: Optional[str] = Field(None, max_length=256)
    last_name: Optional[str] = Field(None, max_length=256)
    is_premium: Optional[bool] = None
    language_code: Optional[str] = Field(None, max_length=32)
