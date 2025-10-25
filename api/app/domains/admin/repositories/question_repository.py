"""
Question repository for admin domain
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from api.app.domains.admin.models.question import Question
from api.app.domains.admin.schemas.question import QuestionCreate


class QuestionRepository:
    """Repository for question data access operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_test_id(self, test_id: int) -> List[Question]:
        """Get all questions for a specific test, ordered by order field"""
        return (
            self.db.query(Question)
            .filter(Question.test_id == test_id)
            .order_by(Question.order)
            .all()
        )

    def get_by_id(self, question_id: int) -> Optional[Question]:
        """Get a question by its ID"""
        return self.db.query(Question).filter(Question.id == question_id).first()

    def create(self, question_data: QuestionCreate, test_id: int) -> Question:
        """Create a new question"""
        question = Question(
            test_id=test_id,
            text=question_data.text,
            order=question_data.order,
            type=question_data.type,
            config=question_data.config,
        )
        self.db.add(question)
        self.db.flush()  # Flush to get the ID
        return question

    def create_bulk(self, questions_data: List[QuestionCreate], test_id: int) -> List[Question]:
        """Create multiple questions for a test"""
        questions = []
        for question_data in questions_data:
            question = Question(
                test_id=test_id,
                text=question_data.text,
                order=question_data.order,
                type=question_data.type,
                config=question_data.config,
            )
            questions.append(question)
            self.db.add(question)
        
        self.db.flush()  # Flush to get the IDs
        return questions

    def update(self, question: Question, question_data: QuestionCreate) -> Question:
        """Update an existing question"""
        question.text = question_data.text
        question.order = question_data.order
        question.type = question_data.type
        question.config = question_data.config
        return question

    def delete(self, question: Question) -> None:
        """Delete a question"""
        self.db.delete(question)

    def delete_by_test_id(self, test_id: int) -> None:
        """Delete all questions for a specific test"""
        self.db.query(Question).filter(Question.test_id == test_id).delete()

    def exists_by_test_and_order(self, test_id: int, order: int, exclude_id: Optional[int] = None) -> bool:
        """Check if a question with the same order exists for a test"""
        query = self.db.query(Question).filter(
            and_(Question.test_id == test_id, Question.order == order)
        )
        if exclude_id:
            query = query.filter(Question.id != exclude_id)
        return query.first() is not None

    def count_by_test_id(self, test_id: int) -> int:
        """Count questions for a specific test"""
        return self.db.query(Question).filter(Question.test_id == test_id).count()

