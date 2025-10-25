"""
Test schemas for admin domain
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator

from .question import QuestionCreate, QuestionUpdate, QuestionResponse


class TestCreate(BaseModel):
    """Schema for creating a test"""
    slug: str = Field(..., min_length=1, max_length=100, description="Unique test identifier")
    name: str = Field(..., min_length=1, max_length=200, description="Test name")
    description: Optional[str] = Field(None, max_length=2000, description="Test description")
    is_active: bool = Field(True, description="Whether test is active")
    questions: List[QuestionCreate] = Field(..., min_items=1, description="Test questions")

    @validator("slug")
    def validate_slug(cls, v: str) -> str:
        """Validate slug format"""
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Slug must contain only alphanumeric characters, hyphens, and underscores")
        return v.lower()

    @validator("questions")
    def validate_questions_order(cls, v: List[QuestionCreate]) -> List[QuestionCreate]:
        """Validate that question orders are unique and sequential"""
        orders = [q.order for q in v]
        if len(orders) != len(set(orders)):
            raise ValueError("Question orders must be unique")
        
        # Check if orders start from 0 or 1 and are sequential
        min_order = min(orders)
        max_order = max(orders)
        expected_orders = set(range(min_order, max_order + 1))
        if set(orders) != expected_orders:
            raise ValueError("Question orders must be sequential")
            
        return v


class TestUpdate(BaseModel):
    """Schema for updating a test"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Test name")
    description: Optional[str] = Field(None, max_length=2000, description="Test description")
    is_active: Optional[bool] = Field(None, description="Whether test is active")
    questions: Optional[List[QuestionCreate]] = Field(None, min_items=1, description="Test questions")

    @validator("questions")
    def validate_questions_order(cls, v: Optional[List[QuestionCreate]]) -> Optional[List[QuestionCreate]]:
        """Validate that question orders are unique and sequential"""
        if v is None:
            return v
            
        orders = [q.order for q in v]
        if len(orders) != len(set(orders)):
            raise ValueError("Question orders must be unique")
        
        # Check if orders start from 0 or 1 and are sequential
        min_order = min(orders)
        max_order = max(orders)
        expected_orders = set(range(min_order, max_order + 1))
        if set(orders) != expected_orders:
            raise ValueError("Question orders must be sequential")
            
        return v


class TestListResponse(BaseModel):
    """Schema for test list response"""
    id: int
    slug: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TestDetailResponse(BaseModel):
    """Schema for test detail response"""
    id: int
    slug: str
    name: str
    description: Optional[str]
    is_active: bool
    questions: List[QuestionResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

