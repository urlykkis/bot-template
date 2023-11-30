from typing import Optional

from pydantic import Field

from src.domain.base.dto import DTO, PatchDTO


class ChannelCreateDTO(DTO):
    """"Сущность для создания канала"""
    chat_id: int
    title: str = Field(..., max_length=32)
    members_count: int = Field(..., ge=0)
    user_id: int = Field(..., ge=0)
    username: Optional[str] = Field(None, max_length=32)


class ChannelDTO(ChannelCreateDTO):
    """Сущность канала"""
    def __repr__(self):
        return f"Channel(id={self.chat_id}, title={self.title}, " \
               f"members={self.members_count})"


class PatchChannelData(PatchDTO):
    """Сущность для редактирования канала"""
    chat_id: int
    title: Optional[str] = Field(None, max_length=256)
    members_count: Optional[int] = Field(None, ge=0)
    username: Optional[str] = Field(None, max_length=32)
    user_id: Optional[int] = Field(None, ge=0)
