from typing import Optional

from pydantic import Field

from src.domain.base.dto.base import DTO


class ChannelDTO(DTO):
    """Сущность канала"""
    chat_id: int
    title: str
    members_count: int
    username: Optional[str] = None
    user_id: int

    def __repr__(self):
        return f"Channel(id={self.chat_id}, title={self.title}, " \
               f"members={self.members_count})"


class ChannelCreateDTO(DTO):
    """"Сущность для создания канала"""
    chat_id: int
    title: str = Field(..., max_length=32)
    members_count: int = Field(..., ge=0)
    user_id: int = Field(..., ge=0)
    username: Optional[str] = Field(None, max_length=32)


class PatchChannelData(DTO):
    """Сущность для редактирования канала"""
    chat_id: int
    title: Optional[str] = Field(None, max_length=256)
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
