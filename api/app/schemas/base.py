"""
Базовые схемы Pydantic
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Базовая схема с общими настройками"""
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
    )


class TimestampMixin(BaseSchema):
    """Миксин для временных меток"""
    created_at: datetime
    updated_at: datetime


class IDMixin(BaseSchema):
    """Миксин для ID"""
    id: int


class BaseResponse(BaseSchema):
    """Базовая схема ответа"""
    success: bool = True
    message: str | None = None


class ErrorResponse(BaseSchema):
    """Схема ошибки"""
    success: bool = False
    error: str
    detail: str | None = None
