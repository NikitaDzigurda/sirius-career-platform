"""
Admin domain schemas
"""
from .test import (
    TestCreate,
    TestUpdate,
    TestListResponse,
    TestDetailResponse,
)
from .question import (
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse,
)

__all__ = [
    "TestCreate",
    "TestUpdate", 
    "TestListResponse",
    "TestDetailResponse",
    "QuestionCreate",
    "QuestionUpdate",
    "QuestionResponse",
]

