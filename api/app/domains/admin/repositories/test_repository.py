"""
Test repository for admin domain
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from api.app.domains.admin.models.test import Test
from api.app.domains.admin.models.question import Question
from api.app.domains.admin.schemas.test import TestCreate, TestUpdate
from api.app.domains.admin.schemas.question import QuestionCreate


class TestRepository:
    """Repository for test data access operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Test]:
        """Get all tests"""
        return self.db.query(Test).order_by(Test.created_at.desc()).all()

    def get_by_slug(self, slug: str) -> Optional[Test]:
        """Get a test by its slug"""
        return self.db.query(Test).filter(Test.slug == slug).first()

    def get_by_id(self, test_id: int) -> Optional[Test]:
        """Get a test by its ID"""
        return self.db.query(Test).filter(Test.id == test_id).first()

    def exists_by_slug(self, slug: str) -> bool:
        """Check if a test with the given slug exists"""
        return self.db.query(Test).filter(Test.slug == slug).first() is not None

    def create(self, test_data: TestCreate) -> Test:
        """Create a new test with questions"""
        # Create the test
        test = Test(
            slug=test_data.slug,
            name=test_data.name,
            description=test_data.description,
            is_active=test_data.is_active,
        )
        self.db.add(test)
        self.db.flush()  # Flush to get the test ID

        # Create questions
        for question_data in test_data.questions:
            question = Question(
                test_id=test.id,
                text=question_data.text,
                order=question_data.order,
                type=question_data.type,
                config=question_data.config,
            )
            self.db.add(question)

        self.db.flush()
        return test

    def update(self, test: Test, test_data: TestUpdate) -> Test:
        """Update an existing test"""
        if test_data.name is not None:
            test.name = test_data.name
        if test_data.description is not None:
            test.description = test_data.description
        if test_data.is_active is not None:
            test.is_active = test_data.is_active

        # If questions are provided, replace all existing questions
        if test_data.questions is not None:
            # Delete existing questions
            self.db.query(Question).filter(Question.test_id == test.id).delete()
            
            # Create new questions
            for question_data in test_data.questions:
                question = Question(
                    test_id=test.id,
                    text=question_data.text,
                    order=question_data.order,
                    type=question_data.type,
                    config=question_data.config,
                )
                self.db.add(question)

        return test

    def delete(self, test: Test) -> None:
        """Delete a test"""
        self.db.delete(test)

    def has_completed_results(self, test_id: int) -> bool:
        """
        Check if a test has any completed results.
        This is used to prevent deletion of tests with results.
        Note: This will be implemented when TestResult model is created.
        For now, returns False to allow deletion.
        """
        # TODO: Implement when TestResult model is available
        # return self.db.query(TestResult).filter(TestResult.test_id == test_id).first() is not None
        return False

    def get_active_tests(self) -> List[Test]:
        """Get all active tests"""
        return self.db.query(Test).filter(Test.is_active == True).order_by(Test.created_at.desc()).all()

    def get_inactive_tests(self) -> List[Test]:
        """Get all inactive tests"""
        return self.db.query(Test).filter(Test.is_active == False).order_by(Test.created_at.desc()).all()

