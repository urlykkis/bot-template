from typing import Any
from unittest.mock import sentinel

from pydantic import BaseModel


class DTO(BaseModel):
    """Основа для сущности"""
    class Config:
        use_enum_values = False
        extra = 'forbid'
        frozen = True
        from_attributes = True


UNSET: Any = sentinel.UNSET
