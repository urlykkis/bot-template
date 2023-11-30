from typing import Any
from unittest.mock import sentinel

from pydantic import BaseModel


class BaseDTO(BaseModel):
    class Config:
        use_enum_values = False
        extra = 'forbid'
        frozen = True
        from_attributes = True


class DTO(BaseDTO):
    """Основа для сущности"""
    def __repr__(self):
        fields = ', '.join(f"{field}={getattr(self, field)}" for field in self.__annotations__)
        return f"{self.__class__.__name__}({fields})"


UNSET: Any = sentinel.UNSET
