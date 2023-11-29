from typing import Optional

from pydantic import Field

from src.domain.base.dto.base import DTO


class ChatDTO(DTO):
    """Сущность чата"""
    chat_id: int
    title: str
    is_super_group: bool
    is_forum: bool
    members_count: int
    user_id: int
    username: Optional[str]

    def __repr__(self):
        return f"Chat(id={self.chat_id}, title={self.title}, members={self.members_count})"


class ChatCreateDTO(DTO):
    """Сущность для создания чата"""
    chat_id: int
    title: str = Field(..., max_length=256)
    is_super_group: bool
    is_forum: bool
    user_id: int = Field(..., ge=0)
    members_count: int = Field(..., ge=0)
    username: Optional[str] = Field(None, max_length=32)


class PatchChatData(DTO):
    """Сущность для редактирования чата"""
    chat_id: int
    title: Optional[str] = Field(None, max_length=256)
    is_super_group: Optional[bool]
    is_forum: Optional[bool] = None
    members_count: Optional[int] = Field(None, ge=0)
    username: Optional[str] = Field(None, max_length=32)
    user_id: Optional[int] = Field(None, ge=0)

    @property
    def updated_data(self) -> dict:
        new_user = self.model_dump()
        new_data = {}

        for key, value in new_user.items():
            if value is not None:
                new_data[key] = value

        return new_data


class ChatMigratedDTO(DTO):
    """Сущность для редактирования чата"""
    old_chat_id: int = Field(..., ge=0)
    new_chat_id: int = Field(..., ge=0)
