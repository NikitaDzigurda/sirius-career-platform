"""
Test model for admin domain
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from api.app.core.database import Base


class Test(Base):
    """
    Test model representing psychological tests (Big Five, MBTI, etc.)
    """
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    questions = relationship("Question", back_populates="test", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_tests_slug", "slug"),
        Index("idx_tests_active", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<Test(id={self.id}, slug='{self.slug}', name='{self.name}')>"

