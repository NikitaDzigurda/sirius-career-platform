"""
Question schemas for admin domain
"""
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, validator


class QuestionCreate(BaseModel):
    """Schema for creating a question"""
    text: str = Field(..., min_length=1, max_length=2000, description="Question text")
    order: int = Field(..., ge=0, description="Question order within test")
    type: str = Field(..., min_length=1, max_length=50, description="Question type")
    config: Dict[str, Any] = Field(..., description="Type-specific configuration")

    @validator("type")
    def validate_question_type(cls, v: str) -> str:
        """Validate question type"""
        allowed_types = ["likert_scale", "binary_choice", "multiple_choice", "text_input"]
        if v not in allowed_types:
            raise ValueError(f"Question type must be one of: {', '.join(allowed_types)}")
        return v

    @validator("config")
    def validate_config(cls, v: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate config based on question type"""
        question_type = values.get("type")
        
        if question_type == "likert_scale":
            required_fields = ["scale", "min_value", "max_value"]
            for field in required_fields:
                if field not in v:
                    raise ValueError(f"Config for likert_scale must include '{field}'")
        elif question_type == "binary_choice":
            required_fields = ["option_a", "option_b"]
            for field in required_fields:
                if field not in v:
                    raise ValueError(f"Config for binary_choice must include '{field}'")
        elif question_type == "multiple_choice":
            if "options" not in v or not isinstance(v["options"], list):
                raise ValueError("Config for multiple_choice must include 'options' as a list")
        elif question_type == "text_input":
            # Text input doesn't require specific config
            pass
            
        return v


class QuestionUpdate(BaseModel):
    """Schema for updating a question"""
    text: Optional[str] = Field(None, min_length=1, max_length=2000, description="Question text")
    order: Optional[int] = Field(None, ge=0, description="Question order within test")
    type: Optional[str] = Field(None, min_length=1, max_length=50, description="Question type")
    config: Optional[Dict[str, Any]] = Field(None, description="Type-specific configuration")

    @validator("type")
    def validate_question_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate question type"""
        if v is None:
            return v
        allowed_types = ["likert_scale", "binary_choice", "multiple_choice", "text_input"]
        if v not in allowed_types:
            raise ValueError(f"Question type must be one of: {', '.join(allowed_types)}")
        return v


class QuestionResponse(BaseModel):
    """Schema for question response"""
    id: int
    test_id: int
    text: str
    order: int
    type: str
    config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

