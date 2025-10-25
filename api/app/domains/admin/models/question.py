"""
Question model for admin domain
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from api.app.core.database import Base


class Question(Base):
    """
    Question model representing individual questions within tests
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)  # e.g., "likert_scale", "binary_choice", "multiple_choice"
    config = Column(JSON, nullable=False)  # Type-specific configuration
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    test = relationship("Test", back_populates="questions")

    # Indexes
    __table_args__ = (
        Index("idx_questions_test_id", "test_id"),
        Index("idx_questions_test_order", "test_id", "order"),
    )

    def __repr__(self) -> str:
        return f"<Question(id={self.id}, test_id={self.test_id}, order={self.order}, type='{self.type}')>"

